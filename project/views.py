# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Viewing the website, through showing 
# all dentists and detailed view of dentists

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Dentist, Appointment, Patient, Treatment
from .forms import PatientUpdateAppointmentForm, DentistUpdateAppointmentForm, PatientCreateAppointmentForm, DentistCreateAppointmentForm, UpdateTreatmentForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginMixin(LoginRequiredMixin): # Redirect to a login
    def get_login_url(self):
        return reverse('login')

class CheckProfile(): # Returning if the user if logged in is a patient or dentist for different options for templates
    def get_context_data(self, **kwargs): # Add variable to context for base.html to get back to profile
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated: 
            try: # Return to check that only patients/dentists can edit their own
                patient = Patient.objects.get(profile__user=user)
                context['profile'] = patient.profile
                context['user_type'] = 'patient'
            except Patient.DoesNotExist:
                try:
                    dentist = Dentist.objects.get(profile__user=user)
                    context['profile'] = dentist.profile
                    context['user_type'] = 'dentist'

                except Dentist.DoesNotExist: # Should not happen
                    context['profile'] = None
                    context['user_type'] = 'None - error'
        else: # If the user is not logged in
            context['profile'] = None
            context['user_type'] = 'None'
        return context

class FrontPageView(CheckProfile, TemplateView):
    template_name = 'project/front_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated: 
            try: # Check if user has a related Patient or Dentist profile
                patient = Patient.objects.get(profile__user=user) # If patient, there will be no need to update treatments, only dentists do so it does not have the field
                context['user_type'] = 'patient' # User is Patient
                context['profile'] = patient.profile # Get the profile of the patient
                context['appointments'] = patient.get_appointments() # Testing context variable
                context['new_appointments'] = patient.get_upcoming_appointments() # Future appointments
                context['past_procedures'] = patient.get_treatment_history() # Appointments that have already happened (in relation to current time)
            except Patient.DoesNotExist:
                try:
                    dentist = Dentist.objects.get(profile__user=user)
                    context['user_type'] = 'dentist'
                    context['profile'] = dentist.profile
                    context['appointments'] = dentist.get_appointments()
                    context['new_appointments'] = dentist.get_upcoming_appointments()
                    context['past_procedures'] = dentist.get_past_procedures()
                    context['need_updates'] = dentist.get_not_updated_procedures()

                    context['need_updates'] = sorted(context['need_updates'], key=lambda a: a.appointment.start)

                    filtered_procedures = [] # Filter out treatments that need updates
                    for treatment in context['past_procedures']:
                        if treatment not in context['need_updates']:
                            filtered_procedures.append(treatment)
                    context['past_procedures'] = filtered_procedures

                except Dentist.DoesNotExist: # Should not happen
                    context['user_type'] = 'none'
                    context['profile'] = None
                    context['appointments'] = []
                    context['new_appointments'] = []
                    context['past_procedures'] = []
        else:
            context['user_type'] = 'none'
            context['profile'] = None
            context['appointments'] = []
            context['new_appointments'] = []
            context['past_procedures'] = []

        context['new_appointments'] = sorted(context['new_appointments'], key=lambda a: a.start) # Sort going from soonest to latest with object a (appointment)
        context['past_procedures'] = sorted(context['past_procedures'], key=lambda a: a.appointment.start) # Treatment needs to access appointment for start time
        return context

class AboutPageView(CheckProfile, TemplateView):
    template_name = 'project/about.html'

class ShowAllDentistsView(CheckProfile, ListView):
    model = Dentist
    template_name = 'project/show_all_dentists.html'
    context_object_name = 'dentists'

class ShowDentistPageView(CheckProfile, DetailView):
    model = Dentist
    template_name = 'project/show_dentist.html'
    context_object_name = 'dentist'

class ShowAllAppointmentsView(CheckProfile, CustomLoginMixin, ListView):
    model = Appointment
    template_name = 'project/all_appointments.html'
    context_object_name = 'appointments'  # This makes the list available as appointments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            try:
                dentist = Dentist.objects.get(profile__user=user)
                context['profile'] = dentist.profile
                context['user_type'] = 'dentist'
                context['new_appointments'] = []
                context['past_procedures'] = []

                for dentists in Dentist.objects.all(): # Get all patients
                    for appointment in dentists.get_upcoming_appointments():
                        context['new_appointments'].append(appointment)
                    for appointment in dentists.get_past_procedures():
                        context['past_procedures'].append(appointment)

                context['new_appointments'] = sorted(context['new_appointments'], key=lambda a: a.start) 
                context['past_procedures'] = sorted(context['past_procedures'], key=lambda a: a.appointment.start)
            except Dentist.DoesNotExist:
                context['profile'] = None
                context['new_appointments'] = []
                context['past_procedures'] = []
        else:
            context['profile'] = None
            context['new_appointments'] = []
            context['past_procedures'] = []
        return context


class AppointmentView(CheckProfile, CustomLoginMixin, DetailView):
    model = Appointment
    template_name = 'project/appointment.html'
    context_object_name = 'appointment'


class MakeAppointment(CheckProfile, CustomLoginMixin, CreateView):
    model = Appointment
    template_name = 'project/create_appointment_form.html'

    def get_form_class(self):
        user = self.request.user
        if Patient.objects.filter(profile__user=user).exists():
            return PatientCreateAppointmentForm
        elif Dentist.objects.filter(profile__user=user).exists():
            return DentistCreateAppointmentForm
        return super().get_form_class()

    def form_valid(self, form):
        user = self.request.user

        # If user is a patient, assign them as the patient
        patient = Patient.objects.filter(profile__user=user).first()
        if patient:
            form.instance.patient = patient

        # If user is a dentist, assign them as the dentist
        dentist = Dentist.objects.filter(profile__user=user).first()
        if dentist:
            form.instance.dentist = dentist

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_appointment', kwargs={'pk': self.object.pk})

    
class UpdateAppointment(CheckProfile, CustomLoginMixin, UpdateView):
    model = Appointment
    template_name = "project/update_appointment_form.html"

    def get_form_class(self):
        user = self.request.user
        if Patient.objects.filter(profile__user=user).exists():
            return PatientUpdateAppointmentForm
        elif Dentist.objects.filter(profile__user=user).exists():
            return DentistUpdateAppointmentForm
        return super().get_form_class()
    
    def form_valid(self, form):
        user = self.request.user

        # If user is a patient, ensure that the patient is not changed
        if Patient.objects.filter(profile__user=user).exists():
            form.instance.patient = Patient.objects.get(profile__user=user)

        return super().form_valid(form)

    def get_object(self):
        appointment = self.kwargs.get('pk') # Get the appointment
        return Appointment.objects.filter(pk=appointment).first()

    def get_success_url(self):
        return reverse('view_appointment', kwargs={'pk': self.object.pk})
    
class TreatmentView(CheckProfile, CustomLoginMixin, DetailView):
    model = Treatment
    template_name = 'project/treatment.html'
    context_object_name = 'treatment'

        
class UpdateTreatment(CheckProfile, CustomLoginMixin, UpdateView):
    model = Treatment
    template_name = "project/update_treatment_form.html"

    def get_form_class(self):
        return UpdateTreatmentForm

    def get_object(self):
        treatment = self.kwargs.get('pk') # Get the appointment
        return Treatment.objects.filter(pk=treatment).first()

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_treatment', kwargs={'pk': self.object.pk})

# class CreateProfile(CreateView):
