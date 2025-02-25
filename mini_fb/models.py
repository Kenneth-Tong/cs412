# File: models.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Creating a model for each profile on the mini_fb project

from django.db import models
from django.urls import reverse

class Profile(models.Model):
    # Data attributes of a profile: most are text fields
    first_name = models.TextField(blank=False) # Seperated first and last names, but will be combined when accessing them for webpages!
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True) # Image for profile
    
    def get_status_messages(self):
        messages = StatusMessage.objects.filter(profile=self)
        return messages

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk}) # Looking at URLS to redirect user to profile they created
    
    # def __str__(self):
    #     '''Return a string representation of this Article object.'''
    #     return f'{self.first_name} {self.last_name}'
    
class StatusMessage(models.Model):
    # Status Message
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.profile}'
    