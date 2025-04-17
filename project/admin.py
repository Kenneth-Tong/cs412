# File: admin.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/12/2025
# Description: Registering profiles for admin

from django.contrib import admin

# Register your models here
from .models import Profile, Patient, Dentist, Appointment, Treatment, BlockedTime

admin.site.register(Patient)
admin.site.register(Profile)
admin.site.register(Dentist)
admin.site.register(Appointment)
admin.site.register(BlockedTime)
admin.site.register(Treatment)