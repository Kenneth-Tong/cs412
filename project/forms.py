# File: forms.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Adding a method of getting information through 
# forms, will be used with views.py

from django import forms
from .models import Appointment, Treatment, Profile, Patient, Dentist

class PatientCreateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['patient']  # Patient is set in the view

class DentistCreateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['dentist']  # Dentist is set in the view

class PatientUpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start', 'end', 'notes'] # Patients can only edit notes and start time

class DentistUpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['patient'] # Dentists can edit everything but patient, they can hand off patients if needed

class UpdateTreatmentForm(forms.ModelForm): # Only dentists can access
    class Meta:
        model = Treatment
        exclude = ['appointment']

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']  # Set the user self

class CreatePatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%Y-%m-%d'])  # YYYY-MM-DD

    class Meta:
        model = Patient
        exclude = ['profile']  # Set the user myself

class CreateDentistForm(forms.ModelForm):
    class Meta:
        model = Dentist
        exclude = ['profile']  # Set the user myself

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['profile']

class UpdateDentistForm(forms.ModelForm):
    class Meta:
        model = Dentist
        exclude = ['profile']