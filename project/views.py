# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/13/2025
# Description: Viewing the website, through showing 
# all dentists and detailed view of dentists

from django.views.generic import TemplateView, ListView, DetailView
from .models import Dentist

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