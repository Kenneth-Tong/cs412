# File: models.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/12/2025
# Description: Models for the patient and interactions for scheduling and dentists

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.urls import reverse

# Profile Background
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_profile")
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    phone = models.TextField(blank=False)
    address = models.TextField(blank=False)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Dentist model
class Dentist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dentist_profile", null=True)
    speciality = models.TextField(blank=False, default='General')
    bio = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('dentists', kwargs={'pk': self.pk})
    
    def get_appointments(self):
        return Appointment.objects.filter(dentist=self)
    
    def get_upcoming_appointments(self): # Get next appointments in the next X days
        return Appointment.objects.filter(dentist=self, start__gt=timezone.now()).order_by('start')

    # def get_todays_appointments(self): # Get appointments today maybe in graphs

    def get_not_updated_procedures(self): # Dentists need to update once procedures are done and are now previous treatments
        need_updates = []
        for treatment in Treatment.objects.filter(appointment__dentist=self):
            if not treatment.get_filled(): # They were not filled out/updated
                need_updates.append(treatment)
        return need_updates

    def get_past_procedures(self): # Get performed appointments
        past_appointments = Appointment.objects.filter(dentist=self, start__lt=timezone.now()) # Get all appointments in the past (from current time)

        for appointment in past_appointments:
            if not appointment.treatments.exists(): # Automatically created one to one reverse relationship to check if a treatment has this appointment
                Treatment.objects.create( # Treatment created if not existing
                    appointment=appointment,
                    procedure="N/A", # Dentist needs to fill out these other aspects
                    tooth_number="N/A",
                    dentist_notes="Auto-generated treatment record"
                )
        return Treatment.objects.filter(appointment__dentist=self)

    def __str__(self):
        if self.profile: # If no profile set
            return f"Dr. {self.profile.first_name} {self.profile.last_name}"
        return "Unnamed Dentist"

# Patient model
class Patient(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="patient_profile", null=True)
    insurance_provider = models.TextField(blank=False)
    date_of_birth = models.DateField()

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_appointments(self):
        return Appointment.objects.filter(patient=self)

    def get_upcoming_appointments(self): # Get next appointments
        return Appointment.objects.filter(patient=self, start__gt=timezone.now()).order_by('start')

    def get_treatment_history(self): #  Will check and create treatment histories based on whether an appointment at the time of being called is in the past
        past_appointments = Appointment.objects.filter(patient=self, start__lt=timezone.now()) # Get all appointments in the past (from current time)

        for appointment in past_appointments:
            if not appointment.treatments.exists(): # Automatically created one to one reverse relationship to check if a treatment has this appointment
                Treatment.objects.create( # Treatment created if not existing
                    appointment=appointment,
                    procedure="N/A", # Dentist needs to fill out these other aspects
                    tooth_number="N/A",
                    dentist_notes="Auto-generated treatment record"
                )
        return Treatment.objects.filter(appointment__patient=self)

    def __str__(self):
        if self.profile: # If no profile set
            return f"{self.profile.first_name} {self.profile.last_name}"
        return "Unnamed Patient"

class BlockedTime(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name='blocked_times')
    start = models.DateTimeField()
    end = models.DateTimeField()
    reason = models.TextField(blank=True)
    
    def __str__(self):
        return f"Blocked: {self.start} to {self.end}"

class Appointment(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    start = models.DateTimeField()
    end = models.DateTimeField()
    notes = models.TextField(blank=True)
    
    def get_absolute_url(self):
        return reverse('appointment_detail', kwargs={'pk': self.pk})
    
    def duration(self): # Minutes lasting
        return (self.end - self.start).total_seconds() / 60
    
    def overlaps_blocked_time(self): # Check appointment scheudle with blocked time
        blocked_times = BlockedTime.objects.filter(dentist=self.dentist)
        for blocked in blocked_times:
            if (self.start < blocked.end and self.end > blocked.start):
                return True
        return False
    
    def clean(self): # Check when appointment is created if the starttime is after endtime OR if appointment times overlap during formvalid() before saving
        if self.start >= self.end:
            raise ValidationError("End time must be later than start time!")
    
        if self.start < timezone.now():
            raise ValidationError("You cannot schedule an appointment in the past.")
        
        overlapping_appointments = Appointment.objects.filter(dentist=self.dentist)
        
        for appointment in overlapping_appointments: # Check if the new appointment overlaps with an existing appointment
            if (self.start < appointment.end and self.end > appointment.start):
                raise ValidationError("This appointment time overlaps with an existing appointment for this dentist.")
    
    def __str__(self):
        if self.patient.profile and self.dentist.profile: # If no profile set
            return f"{self.patient} with {self.dentist} at {self.start}"
        return f"Unassigned personel"

class Treatment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='treatments')
    procedure = models.TextField(blank=False)
    tooth_number = models.TextField(blank=False)
    dentist_notes = models.TextField(blank=True, default="No notes from dentist yet.")

    def get_filled(self): # If the treatment was filled out by the dentist
        return (self.procedure != "N/A" and self.tooth_number != "N/A" and self.dentist_notes != "Auto-generated treatment record")

    def __str__(self):
        return f"{self.appointment}: {self.procedure} on tooth {self.tooth_number}"