# voting/urls.py
from django.urls import path
from .views import VoteCreateView, VotingResultView

urlpatterns = [
    path('vote/', VoteCreateView.as_view(), name='vote'),  # Endpoint for submitting a vote
    path('results/today/', VotingResultView.as_view(), name='voting-results'),  # Endpoint for retrieving today's voting results
]

