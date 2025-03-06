# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Two methods of viewing the website, through showing all profiles or selecting for a profile and selecting a template
# associated with each type of response that the view.py retrieves

from django.urls import reverse
from .models import Profile, Image, StatusImage, StatusMessage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all blog articles.'''

    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file, multiple profiles in a list

class ShowProfilePageView(DetailView):
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_profile.html' # Only showing one profile type of template, no table
    context_object_name = 'profile' # how to find the data in the template file, only one profile

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    '''A view to create a new comment and save it to the database.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment
        object before saving it to the database.
        '''

		# instrument our code to display form fields: 
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK

        sm = form.save() # Saving the message to the database

        files = self.request.FILES.getlist('files') # Read form files
        
        for file in files:
            image = Image.objects.create(profile=sm.profile, image_file=file)
            StatusImage.objects.create(image=image, status_message=sm)

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
            
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # create and return a URL:
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('show_profile', kwargs={'pk':pk})

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView): # Delete a status message
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

class UpdateStatusMessageView(UpdateView): # Update a status message on someone's profile
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_message_form.html"
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Redirect to the profile page of the status message's owner after updating.'''
        # Get the profile associated with the status message
        
        profile = self.object.profile
        # Reverse the URL for the profile page
        return reverse('show_profile', kwargs={'pk': profile.pk})