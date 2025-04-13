# File: urls.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/12/2025
# Description: Created a way for a browser to access each type of response from the server via
# a url which will then be processed by the views.py

from django.urls import path
from .views import *
# from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', FrontPage.as_view(), name="front_page"),
]