# File: forms.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Adding a method of getting information through 
# forms, will be used with views.py

from django import forms
from .models import Appointment, Treatment, Profile, Patient, Dentist, BlockedTime

class PatientCreateAppointmentForm(forms.ModelForm):
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model = Appointment
        exclude = ['patient']  # Patient is set in the view

class DentistCreateAppointmentForm(forms.ModelForm):
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    input_formats=['%Y-%m-%dT%H:%M']
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

class CreatePatientForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model = Patient
        exclude = ['user']  # Set the user myself

class CreateDentistForm(forms.ModelForm):
    class Meta:
        model = Dentist
        exclude = ['user']  # Set the user myself

class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user']

class UpdateDentistForm(forms.ModelForm):
    class Meta:
        model = Dentist
        exclude = ['user']

class CreateBlockedTimesForm(forms.ModelForm):
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'styled-datetime',
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    input_formats=['%Y-%m-%dT%H:%M']
    class Meta:
        model = BlockedTime
        exclude = ['dentist']

class UpdateBlockedTimesForm(forms.ModelForm):
    class Meta:
        model = BlockedTime
        exclude = ['dentist'] # Dentists can change their own times/reason