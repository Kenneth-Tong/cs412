# File: admin.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/3/2025
# Description: Adding voter  to admin

from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Voter)