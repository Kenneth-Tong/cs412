# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Two methods of viewing the website, through showing all profiles or selecting for a profile and selecting a template
# associated with each type of response that the view.py retrieves

from .models import Profile
from django.views.generic import ListView, DetailView

class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all blog articles.'''

    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file, multiple profiles in a list

class ShowProfilePageView(DetailView):
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_profile.html' # Only showing one profile type of template, no table
    context_object_name = 'profile' # how to find the data in the template file, only one profile
