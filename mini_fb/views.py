# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Two methods of viewing the website, through showing all profiles or selecting for a profile and selecting a template
# associated with each type of response that the view.py retrieves

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Profile, Image, StatusImage, StatusMessage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class CustomLoginMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('login')
    
    def get_context_data(self, **kwargs): # Add variable to context for base.html to get back to profile
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=self.request.user).first()
        return context

class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all blog articles.'''

    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file, multiple profiles in a list

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        # Simply return the profile based on the pk in the URL
        return Profile.objects.get(pk=self.kwargs['pk'])
    
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CustomLoginMixin, CreateView):
    context_object_name = 'status_message'
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def form_valid(self, form): # Use the correct profile
        profile = Profile.objects.filter(user=self.request.user).first()
        form.instance.profile = profile
        sm = form.save() # Saving the message to the database
        
        files = self.request.FILES.getlist('files') # Read form files
        for file in files:
            image = Image.objects.create(profile=sm.profile, image_file=file)
            StatusImage.objects.create(image=image, status_message=sm)
            
        return super().form_valid(form)

    def get_success_url(self):
        profile = Profile.objects.filter(user=self.request.user).first()
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
class UpdateProfileView(CustomLoginMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    # def dispatch(self, request, *args, **kwargs):
    #     # profile = Profile.objects.filter(user=self.request.user).first()
    #     # if profile != ____:
    #     #     return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    #     return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()
    

class DeleteStatusMessageView(CustomLoginMixin, DeleteView): # Delete a status message
    '''A view to delete a message and remove it from the database.'''

    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status_message'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this status_message
        pk = self.kwargs.get('pk')
        status_message = StatusMessage.objects.get(pk=pk)
        
        # find the profile to which this status_message is related by FK
        profile = status_message.profile
        
        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        if status_message.profile.user != request.user:
            return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': status_message.profile.pk}))
        return super().dispatch(request, *args, **kwargs)

class UpdateStatusMessageView(CustomLoginMixin, UpdateView): # Update a status message on someone's profile
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_message_form.html"
    context_object_name = 'status_message'

    def get_success_url(self):
        # Get the profile associated with the status message
        
        profile = self.object.profile
        # Reverse the URL for the profile page
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        if status_message.profile.user != request.user:
            return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': status_message.profile.pk}))
        return super().dispatch(request, *args, **kwargs)

class CreateFriendView(CustomLoginMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = request.user.profile
        other_pk = kwargs.get('other_pk')
        other_profile = Profile.objects.get(pk=other_pk)
        
        profile.add_friend(other_profile) # Add the friend relationship
        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    
class ShowFriendSuggestionsView(CustomLoginMixin, DetailView):
    # A view to show friend suggestions for a profile
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'  # So we can access it in the template as "profile"
    
    def get_object(self):
        return Profile.objects.filter(user=self.request.user).first()
    
class ShowNewsFeedView(CustomLoginMixin, DetailView):
    # A view to show the news feed for a profile
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self): # Filter based on user
        return Profile.objects.filter(user=self.request.user).first()
    
    def get_context_data(self, **kwargs): # Add variable to context for base.html to get back to profile
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context