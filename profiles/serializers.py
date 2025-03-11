from rest_framework import serializers
from .models import Profile
from skills.models import Skill
from accounts.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'