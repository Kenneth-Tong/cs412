from django.urls import path
from .views import ShowAllProfiles, ShowProfilePageView

urlpatterns = [
    path('', ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('show_all_profiles', ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),# new
]