# File: models.py
# Author: Kenneth Tong (ktong22@bu.edu), 2/17/2025
# Description: Creating a model for each profile on the mini_fb project

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    # Data attributes of a profile: most are text fields
    first_name = models.TextField(blank=False) # Seperated first and last names, but will be combined when accessing them for webpages!
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    image_url = models.URLField(blank=True) # Image for profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_status_messages(self):
        messages = StatusMessage.objects.filter(profile=self)
        return messages

    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk}) # Looking at URLS to redirect user to profile they created
    
    def get_friends(self):
        friends_as_profile1 = Friend.objects.filter(profile1=self) # If profile 1 is this person's profile
        friends_as_profile2 = Friend.objects.filter(profile2=self)
        friends = []  # List of friends

        # Add profile2 when self is profile1
        for friend in friends_as_profile1:
            if friend.profile2 != self:  
                friends.append(friend.profile2)
            
        # Add profile1 when self is profile2
        for friend in friends_as_profile2:
            if friend.profile1 != self:
                friends.append(friend.profile1)
        return friends

    def add_friend(self, other):
        # Prevent self-friending
        if self == other:
            return

        # Check if the friendship already exists (either direction)
        if Friend.objects.filter(profile1=self, profile2=other).exists() or Friend.objects.filter(profile1=other, profile2=self).exists():
            return

        # Create new Friend relationship
        Friend.objects.create(profile1=self, profile2=other)
        return
    
    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk=self.pk) # All but this profile
        current_friends = self.get_friends() # Make sure not to include friends already there
        profile = []

        for friend in all_profiles:
            if not friend in current_friends:
                profile.append(friend)
        return profile
    
    def get_news_feed(self):
        friends = self.get_friends() # Get the friends list
        profile = []
        for friend in friends:
            profile.append(friend)
        
        profile.append(self)
        messages = StatusMessage.objects.filter(profile__in=profile).order_by('-timestamp') # Order by time
        return messages

    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name}'
    
class StatusMessage(models.Model):
    # Status Message
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def get_images(self):
        status_images = StatusImage.objects.filter(status_message=self)
        image_list = []
        for status_image in status_images:
            image_list.append(status_image.image)
        return image_list
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.profile.first_name} {self.profile.last_name}: {self.message}'

class Image(models.Model): # Holds the image and upload time to a profile
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True, upload_to='uploads/')
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Image({self.image_file.url}, Caption={self.caption})'

class StatusImage(models.Model): # Ways to find images that relate to a status message and the other way
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        return f'StatusImage(StatusMessage={self.status_message.pk}, Image={self.image.pk})'

class Friend(models.Model): # Friends connecting two nodes in a network
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True) # Time friendship made

    def __str__(self):
        return f'{self.profile1} & {self.profile2}'