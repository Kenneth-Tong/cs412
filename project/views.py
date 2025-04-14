# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Viewing the website, through showing 
# all dentists and detailed view of dentists

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Dentist, Appointment, Patient
from .forms import CreateAppointmentForm, UpdateFormForm
from django.urls import reverse

class FrontPageView(TemplateView):
    template_name = 'project/front_page.html'

class AboutPageView(TemplateView):
    template_name = 'project/about.html'

class ShowAllDentistsView(ListView):
    model = Dentist
    template_name = 'project/show_all_dentists.html'
    context_object_name = 'dentists'

class ShowDentistPageView(DetailView):
    model = Dentist
    template_name = 'project/show_dentist.html'
    context_object_name = 'dentist'

class AppointmentView(DetailView):
    model = Appointment
    template_name = 'project/appointment.html'
    context_object_name = 'appointment'

class MakeAppointment(CreateView):
    model = Appointment
    form_class = CreateAppointmentForm
    template_name = 'project/create_appointment_form.html'

    def form_valid(self, form):
        patient = Patient.objects.filter(user=self.request.user).first()
        form.instance.patient = patient
        return super().form_valid(form)
    
    def get_success_url(self):
        # Reverse the URL for the profile page
        return reverse('dashboard')

class UpdateAppointment(UpdateView):
    template_name = "project/update_appointment_form.html"

    def get_object(self):
        return Appointment.objects.filter(user=self.request.user).first()