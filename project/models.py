# File: models.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/12/2025
# Description: Models for the patient  and interactions for scheduling and dentists

from django.db import models
from django.contrib.auth.models import User

# Patient Profile
class Patient(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    date_of_birth = models.DateField(blank=False)
    phone_number = models.TextField(blank=False)
    image_file = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')

    def get_appointments(self):
        return self.appointments.all()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Dentist
class Dentist(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    speciality = models.TextField(blank=False)
    email = models.TextField(blank=False)
    bio = models.TextField(blank=False)
    image_file = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_schedule(self): # Each dentist has a schedule
        return self.schedule.first()

    def get_appointments(self):
        return self.appointments.all()

    def __str__(self):
        return f'Dr. {self.first_name} {self.last_name}'


# Schedule for Dentist
class Schedule(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name='schedule')

    def get_open_slots(self):
        available_appointments = []
        for appointment in self.appointments.filter(schedule=self):
            if appointment.is_open(self): # If there is no patient assigned in the time slot, it is open
                available_appointments.append(appointment)
        return available_appointments

    def get_filled_appointments(self):
        taken_appointments = []
        for appointment in self.appointments.filter(schedule=self):
            if not appointment.is_open(self): # If there is  patient assigned in the time slot, it is filled
                taken_appointments.append(appointment)
        return taken_appointments
    
    def __str__(self):
        return f"Schedule for Dr. {self.dentist.first_name} {self.dentist.last_name}"


# Appointment — if patient is not set, it's an open slot
class Appointment(models.Model):
    appointment_time = models.DateTimeField(blank=True)
    note = models.TextField(blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name='appointments')

    def is_open(self):
        if self.patient:
            return False
        return True

    def __str__(self):
        if self.patient:
            return f"{self.patient.first_name} with Dr. {self.dentist.last_name} at {self.appointment_time}"
        return f"Open slot with Dr. {self.dentist.last_name} at {self.appointment_time}"


# Treatment History
class TreatmentHistory(models.Model):
    procedure = models.TextField()
    tooth_number = models.TextField()
    tooth_status = models.TextField()
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='treatments')

    def __str__(self):
        return f"Treatment for {self.appointment.patient.first_name} on {self.appointment.appointment_time}"
