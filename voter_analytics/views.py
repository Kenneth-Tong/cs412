# File: views.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/3/2025
# Description: Views for organizing data to send
# to the template

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Voter
import plotly.graph_objs as go # type: ignore
import plotly # type: ignore

class VoterListView(ListView):
    """View to list and filter Voter records."""
    template_name = 'voters/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter voters based on form inputs."""
        queryset = super().get_queryset().order_by('last_name')
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Elections
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        
        # Apply filters if selected
        if voter_score and voter_score != "Any":
            queryset = queryset.filter(voter_score=voter_score)
        if party:
            queryset = queryset.filter(party_affiliation__iexact=party) # Insensitive match regardless of spaces
        if min_dob and min_dob != "Any":
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob and max_dob != "Any":
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score and voter_score != "Any":
            queryset = queryset.filter(voter_score=voter_score)
        if v20state == "on":
            queryset = queryset.filter(v20state=True)
        if v21town == "on":
            queryset = queryset.filter(v21town=True)
        if v21primary == "on":
            queryset = queryset.filter(v21primary=True)
        if v22general == "on":
            queryset = queryset.filter(v22general=True)
        if v23town == "on":
            queryset = queryset.filter(v23town=True)

        return queryset
    
    def get_context_data(self, **kwargs):
        """Provide additional context to the voter detail template."""
        context = super().get_context_data(**kwargs)
        context['years'] = [f"{year}-01-01" for year in range(1900, 2025)] # Fix to ensure formatting
        context['scores'] = range(0, 6)
        return context

class VoterDetailView(DetailView):
    """View to show details of a single Voter."""
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

class VoterGraphView(ListView):
    """View to display voter graphs"""
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        """Filter voters based on form inputs."""
        queryset = super().get_queryset().order_by('last_name')
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')

        # Elections
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')
        
        # Apply filters if selected
        if voter_score and voter_score != "Any":
            queryset = queryset.filter(voter_score=voter_score)
        if party:
            queryset = queryset.filter(party_affiliation__iexact=party) # Insensitive match regardless of spaces
        if min_year and min_year != "Any":
            queryset = queryset.filter(date_of_birth__gte=min_year)
        if max_year and max_year != "Any":
            queryset = queryset.filter(date_of_birth__lte=max_year)
        if voter_score and voter_score != "Any":
            queryset = queryset.filter(voter_score=voter_score)
        if v20state == "on":
            queryset = queryset.filter(v20state=True)
        if v21town == "on":
            queryset = queryset.filter(v21town=True)
        if v21primary == "on":
            queryset = queryset.filter(v21primary=True)
        if v22general == "on":
            queryset = queryset.filter(v22general=True)
        if v23town == "on":
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        context['years'] = [f"{year}-01-01" for year in range(1900, 2025)] # Fix to ensure formatting
        context['scores'] = range(0, 6)
        
        # 1. Birth Year Histogram
        birth_years = [v.date_of_birth.year for v in voters if v.date_of_birth]
        year_counts = {}
        for year in birth_years:
            year_counts[year] = year_counts.get(year, 0) + 1
        
        birth_fig = go.Figure(
            data=[go.Bar(
                x=list(year_counts.keys()),
                y=list(year_counts.values())
            )]
        )
        birth_fig.update_layout(title='Voters by Birth Year')
        context['birth_graph'] = plotly.offline.plot(
            {"data": birth_fig}, 
            auto_open=False, 
            output_type="div"
        )

        # 2. Party Affiliation Pie Chart
        party_data = voters.values('party_affiliation').annotate(
            count=Count('id')
        ).order_by('-count')
        
        party_fig = go.Figure(
            data=[go.Pie(
                labels=[p['party_affiliation'] or 'Unknown' for p in party_data],
                values=[p['count'] for p in party_data]
            )]
        )
        party_fig.update_layout(title='Party Affiliation')
        context['party_graph'] = plotly.offline.plot(
            {"data": party_fig},
            auto_open=False,
            output_type="div"
        )

        # 3. Election Participation Bar Chart
        election_counts = [
            ('2020 State', voters.filter(v20state=True).count()),
            ('2021 Town', voters.filter(v21town=True).count()),
            ('2021 Primary', voters.filter(v21primary=True).count()),
            ('2022 General', voters.filter(v22general=True).count()),
            ('2023 Town', voters.filter(v23town=True).count())
        ]
        
        election_fig = go.Figure(
            data=[go.Bar(
                x=[e[0] for e in election_counts],
                y=[e[1] for e in election_counts]
            )]
        )
        election_fig.update_layout(title='Election Participation')
        context['election_graph'] = plotly.offline.plot(
            {"data": election_fig},
            auto_open=False,
            output_type="div"
        )

        return context