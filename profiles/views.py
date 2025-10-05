from rest_framework import viewsets, permissions
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework.routers import DefaultRouter
from .permissions import IsSelfForWrite
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsSelfForWrite]

    def perform_create(self, serializer):
        # Attach the logged-in user to the created instance if needed
        serializer.save()