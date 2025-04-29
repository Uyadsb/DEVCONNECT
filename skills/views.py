from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import SkillSerializer
from .models import Skill

# Create your views here.
class SkillViewSets(viewsets.ModelViewSet):
    query_set = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
