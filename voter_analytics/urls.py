# File: urls.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/3/2025
# Description: Url for displaying different url pages

from django.urls import path
from .views import VoterListView, VoterDetailView, VoterGraphView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', VoterGraphView.as_view(), name='graphs'),
]
