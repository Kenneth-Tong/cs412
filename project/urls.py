# File: urls.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/12/2025
# Description: Created a way for a browser to access each type of response from the server via
# a url which will then be processed by the views.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.FrontPageView.as_view(), name='dashboard'),
    path('dashboard/', views.FrontPageView.as_view(), name='dashboard'),
    path('dentists/', views.ShowAllDentistsView.as_view(), name='show_all_dentists'),
    path('dentists/<int:pk>/', views.ShowDentistPageView.as_view(), name='show_dentist'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('all_appointments/', views.ShowAllAppointmentsView.as_view(), name='all_appointments'),
    path('appointment/<int:pk>/', views.AppointmentView.as_view(), name='view_appointment'),
    path('appointment/new/', views.MakeAppointment.as_view(), name='make_appointment'),
    path('appointment/<int:pk>/update', views.UpdateAppointment.as_view(), name='update_appointment'), 
    path('treatment/<int:pk>/', views.TreatmentView.as_view(), name='view_treatment'), 
    path('treatment/<int:pk>/update', views.UpdateTreatment.as_view(), name='update_treatment'), 
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html', next_page='dashboard'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)