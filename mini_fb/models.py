# File: models.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Creating a model for each profile on the mini_fb project

from django.db import models

class Profile(models.Model):
    # Data attributes of a profile: most are text fields
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True) # Image for profile
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name}'