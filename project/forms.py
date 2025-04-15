# File: forms.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Adding a method of getting information through 
# forms, will be used with views.py

from django import forms
from .models import Patient, Dentist, Appointment

class CreateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['patient']  # Patient making appointment already included automatically

class UpdateFormForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['patient'] # Cannot edit appointments not part of their appointment list