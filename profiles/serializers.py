from rest_framework import serializers
from .models import Profile
from skills.serializers import SkillSerializer
from accounts.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    user = UserSerializer()
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'skills', 'avatar']