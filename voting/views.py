# voting/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from .models import Menu, Vote
from django.db.models import Count
from .serializers import VoteSerializer

class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def perform_create(self, serializer):
        user = self.request.user
        today = datetime.now().date() # Get today's date
        menu_id = self.request.data.get('menu_id')  # Retrieve menu ID from request data
        menu = Menu.objects.get(id=menu_id)  # Get the Menu instance based on ID

        # Check if the user has already voted today
        if Vote.objects.filter(user=user, voted_at=today).exists():
            raise ValidationError({"datail":"You are already voted today"}, code=status.HTTP_400_BAD_REQUEST) # Return an error if already voted
        
        serializer.save(user=user, menu=menu)  # Save the vote with the current user and menu

class VotingResultView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request):
        today = datetime.now().date()  # Get today's date
        votes = Vote.objects.filter(voted_at=today)  # Filter votes for today
        # Aggregate votes by menu and count them, then order by vote count
        results = votes.values('menu__restaurant__name').annotate(vote_count=Count('id')).order_by('-vote_count')
        return Response(results)  # Return the aggregated results
