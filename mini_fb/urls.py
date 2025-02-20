# File: urls.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Created a way for a browser to access each type of response from the server via
# a url which will then be processed by the views.py

from django.urls import path
from .views import ShowAllProfiles, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('show_all_profiles', ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),# new
]