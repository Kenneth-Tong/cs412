# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Viewing the website, through showing 
# all dentists and detailed view of dentists

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Dentist, Appointment, Patient
from .forms import CreateAppointmentForm
from django.urls import reverse

class FrontPageView(TemplateView):
    template_name = 'project/front_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated: 
            try: # Check if user has a related Patient or Dentist profile
                patient = Patient.objects.get(profile__user=user)
                context['user_type'] = 'patient'
                context['profile'] = patient.profile
                context['appointments'] = patient.get_appointments()
                template_name = 'project/patient_dash.html'
            except Patient.DoesNotExist:
                try:
                    dentist = Dentist.objects.get(profile__user=user)
                    context['user_type'] = 'dentist'
                    context['profile'] = dentist.profile
                    context['appointments'] = dentist.get_appointments()
                    template_name = 'project/dentist_dash.html'
                except Dentist.DoesNotExist: # Should not happen
                    context['user_type'] = 'none'
                    context['profile'] = None
                    context['appointments'] = []
        else:
            context['user_type'] = 'none'
            context['profile'] = None
            context['appointments'] = []
        return context

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
    
    def get_success_url(self): # Reverse the URL for the profile page
        return reverse('dashboard')

class UpdateAppointment(UpdateView):
    template_name = "project/update_appointment_form.html"

    def get_object(self):
        patient = Patient.objects.filter(user=self.request.user).first()
        return Appointment.objects.filter(patient=patient).first()
    
# class CreateProfile(CreateView):