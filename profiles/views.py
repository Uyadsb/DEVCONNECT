from rest_framework import viewsets, permissions
from .serializers import ProfileSerializer
from django.contrib.auth.decorators import login_required 
from .models import Profile
from rest_framework.routers import DefaultRouter


# Create your views here.
class ProfileViewSets(viewsets.ModelViewSet):
    serializers_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  
        
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)