# File: urls.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Created a way for a browser to access each type of response from the server via
# a url which will then be processed by the views.py

from django.urls import path
from .views import ShowAllProfiles, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView

urlpatterns = [
    path('', ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('show_all_profiles', ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),# new
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
	path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status_message'), 
	path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status_message'), 
]