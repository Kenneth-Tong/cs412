# File: forms.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/25/2025
# Description: Adding a method of getting information through forms, will be used
# with views.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = "__all__"


class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a message to the database.'''

    class Meta:
        '''associate this form with the Message model; select fields'''
        model = StatusMessage
        fields = ['message']  # Which fields from model should we use

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['first_name', 'last_name',] # Everything except name

class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        exclude = ['profile'] # Cannot edit the profile who said it!