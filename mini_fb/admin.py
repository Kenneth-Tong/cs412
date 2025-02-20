# File: admin.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Adding another type of model as a Profile for Django

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)