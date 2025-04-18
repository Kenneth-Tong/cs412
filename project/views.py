# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Viewing the website, through showing 
# all dentists and detailed view of dentists

from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dentist, Appointment, Patient, Treatment, Profile
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

class CustomLoginMixin(LoginRequiredMixin): # Redirect to a login
    def get_login_url(self):
        return reverse('login')

class CheckProfile(): # Returning if the user if logged in is a patient or dentist for different options for templates
    def get_context_data(self, **kwargs): # Add variable to context for base.html to get back to profile
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated: 
            try: # Return to check that only patients/dentists can edit their own
                patient = Patient.objects.get(user=user)
                context['profile'] = patient
                context['user_type'] = 'patient'
            except Patient.DoesNotExist:
                try:
                    dentist = Dentist.objects.get(user=user)
                    context['profile'] = dentist
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
                patient = Patient.objects.get(user=user) # If patient, there will be no need to update treatments, only dentists do so it does not have the field
                context['appointments'] = patient.get_appointments() # Testing context variable
                context['new_appointments'] = patient.get_upcoming_appointments() # Future appointments
                context['past_procedures'] = patient.get_treatment_history() # Appointments that have already happened (in relation to current time)
            except Patient.DoesNotExist:
                try:
                    dentist = Dentist.objects.get(user=user)
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
                    context['appointments'] = []
                    context['new_appointments'] = []
                    context['past_procedures'] = []
        else:
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
                dentist = Dentist.objects.get(user=user)
                context['profile'] = dentist
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
        if Patient.objects.filter(user=user).exists():
            return PatientCreateAppointmentForm
        elif Dentist.objects.filter(user=user).exists():
            return DentistCreateAppointmentForm
        return super().get_form_class()
    
    def get_form(self, form_class=None): # Set the instances of patient and dentist before clean checks it before form_valid
        form = super().get_form(form_class)

        user = self.request.user
        if Patient.objects.filter(user=user).exists():
            form.instance.patient = Patient.objects.filter(user=user).first()
        elif Dentist.objects.filter(user=user).exists():
            form.instance.dentist = Dentist.objects.filter(user=user).first()

        return form

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_appointment', kwargs={'pk': self.object.pk})

    
class UpdateAppointment(CheckProfile, CustomLoginMixin, UpdateView):
    model = Appointment
    template_name = "project/update_appointment_form.html"

    def get_form_class(self):
        user = self.request.user
        if Patient.objects.filter(user=user).exists():
            return PatientUpdateAppointmentForm
        elif Dentist.objects.filter(user=user).exists():
            return DentistUpdateAppointmentForm
        return super().get_form_class()
    
    def form_valid(self, form):
        user = self.request.user

        # If user is a patient, ensure that the patient is not changed
        if Patient.objects.filter(user=user).exists():
            form.instance.patient = Patient.objects.get(user=user)

        return super().form_valid(form)

    def get_object(self):
        appointment = self.kwargs.get('pk') # Get the appointment
        return Appointment.objects.filter(pk=appointment).first()

    def get_success_url(self):
        return reverse('view_appointment', kwargs={'pk': self.object.pk})
    

class DeleteAppointmentView(CheckProfile, CustomLoginMixin, DeleteView):
    template_name = "project/delete_appointment.html"
    model = Appointment
    context_object_name = 'appointment'
    
    def get_success_url(self): # Go to dashboard after deleting an appointment
        return reverse('dashboard')

    def dispatch(self, request, *args, **kwargs): # Is profile allowed to delete this
        appointment = self.get_object()
        user = request.user

        try: # Attempt to get the profile (patient or dentist) associated with the user
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            patient = None

        try:
            dentist = Dentist.objects.get(user=user)
        except Dentist.DoesNotExist:
            dentist = None

        # Only allow if the user is the patient or dentist on the appointment
        if appointment.patient != patient and appointment.dentist != dentist:
            return HttpResponseRedirect(reverse('dashboard'))
        
        return super().dispatch(request, *args, **kwargs)


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


class DeleteTreatmentView(CheckProfile, CustomLoginMixin, DeleteView):
    template_name = "project/delete_treatment.html"
    model = Treatment
    context_object_name = 'treatment'
    
    def get_success_url(self): # Go to dashboard after deleting an appointment
        return reverse('dashboard')

    def dispatch(self, request, *args, **kwargs): # Is profile allowed to delete this
        treatment = self.get_object()
        user = request.user

        try:
            patient = Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            patient = None

        try:
            dentist = Dentist.objects.get(user=user)
        except Dentist.DoesNotExist:
            dentist = None

        # Only allow if the profile is the patient or dentist on the appointment
        if treatment.appointment.patient != patient and treatment.appointment.dentist != dentist:
            return HttpResponseRedirect(reverse('dashboard'))
        
        print('before dispatch')
    
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        treatment = self.get_object()
        appointment = treatment.appointment
        appointment.delete() # Delete the appointment too so it doesn't keep creating treatment histories

        return super().form_valid(form)
    

class ProfileView(CheckProfile, CustomLoginMixin, DetailView):
    model = Profile
    template_name = 'project/base_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user.project_profile
        raise ValidationError("No Profile Associated")
    
    def get_context_data(self, **kwargs): # Get the profile's relationship model
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            if context['user_type'] == 'dentist':
                dentist = Dentist.objects.get(user=user)
                context['dentist'] = dentist
            elif context['user_type'] == 'patient':
                patient = Patient.objects.get(user=user)
                context['patient'] = patient
        return context


class CreateProfileView(CreateView):
    template_name = "project/create_profile_form.html"
    
    def get_form_class(self):
        user_type = self.request.GET.get('type')
        if user_type == 'patient':
            return CreatePatientForm
        elif user_type == 'dentist':
            return CreateDentistForm
        
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        
        form.instance.user = user # Attach the user to the profile
        
        login(self.request, user)
        
        return super().form_valid(form) # Saving form
  
    def get_success_url(self):
        return reverse('dashboard')


class UpdateProfile(CheckProfile, CustomLoginMixin, UpdateView):
    template_name = "project/update_profile_form.html"

    def get_form_class(self):
        obj = self.get_object()
        
        if isinstance(obj, Dentist):
            return UpdateDentistForm
        elif isinstance(obj, Patient):
            return UpdatePatientForm
        
        raise ValueError("Form type does not match the object being updated.")
    
    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            is_patient = Patient.objects.filter(user=user).exists()
            is_dentist = Dentist.objects.filter(user=user).exists()

            if is_dentist:
                return Dentist.objects.get(user=user)
            elif is_patient:
                return Patient.objects.get(user=user)
            
        return None

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_profile', kwargs={'pk': self.object.pk})
    

class BlockedTimeListView(CheckProfile, CustomLoginMixin, ListView):
    model = BlockedTime
    template_name = 'project/blocked_time_list.html'
    context_object_name = 'blocked_times'


class BlockedTimeView(CheckProfile, CustomLoginMixin, DetailView):
    model = BlockedTime
    template_name = 'project/blocked_time.html'
    context_object_name = 'blocked_time'


class CreateBlockedTimeView(CheckProfile, CustomLoginMixin, CreateView):
    model = BlockedTime
    template_name = 'project/create_blocked_time.html'
    form_class = CreateBlockedTimesForm

    def form_valid(self, form):
        user = self.request.user

        dentist = Dentist.objects.filter(user=user).first() # Set dentist to form
        if dentist:
            form.instance.dentist = dentist

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blocked_time_view', kwargs={'pk': self.object.pk})


class UpdateBLockedTimeView(CheckProfile, CustomLoginMixin, UpdateView):
    model = BlockedTime
    template_name = "project/update_blocked_time_form.html"
    form_class = UpdateBlockedTimesForm

    def get_object(self):
        blocked_time = self.kwargs.get('pk') # Get the blocked time
        return BlockedTime.objects.filter(pk=blocked_time).first()

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blocked_time_view', kwargs={'pk': self.object.pk})
    

class DeleteBlockedTimeView(CheckProfile, CustomLoginMixin, DeleteView):
    template_name = "project/delete_blocked_time.html"
    model = BlockedTime
    context_object_name = 'blocked_time'
    
    def get_success_url(self): # Go to dashboard after deleting an appointment
        return reverse('blocked_time_list')

    def dispatch(self, request, *args, **kwargs): # Is profile allowed to delete this
        blocked_time = self.get_object()
        user = request.user

        try:
            dentist = Dentist.objects.get(user=user)
        except Dentist.DoesNotExist:
            dentist = None

        # Only allow if the user is the dentist on the blocked_time
        if blocked_time.dentist != dentist:
            return HttpResponseRedirect(reverse('dashboard'))
        
        return super().dispatch(request, *args, **kwargs)
