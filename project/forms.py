# File: forms.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Adding a method of getting information through 
# forms, will be used with views.py

from django import forms
from .models import Appointment

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
        fields = ['start', 'notes'] # Patients can only edit notes and start time

class DentistUpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['patient'] # Dentists can edit everything but patient, they can hand off patients if needed

