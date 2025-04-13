# File: urls.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/12/2025
# Description: Created a way for a browser to access each type of response from the server via
# a url which will then be processed by the views.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.FrontPageView.as_view(), name='dashboard'),
    path('dashboard/', views.FrontPageView.as_view(), name='dashboard'),
    path('dentists/', views.ShowAllDentistsView.as_view(), name='show_all_dentists'),
    path('dentists/<int:pk>/', views.ShowDentistPageView.as_view(), name='show_dentist'),
    path('about/', views.AboutPageView.as_view(), name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)