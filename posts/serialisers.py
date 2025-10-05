from rest_framework import serializers
from .models import File, Post, Comment, Like
from accounts.serializers import UserSerializer

class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']

        
class PostSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    file = serializers.FileField(required=False)
    user = UserSerializer(read_only=True)  # Add this
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'picture', 'file', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'post': {'required': True},
            'content': {'required': True}
        }
        

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']
        read_only_fields = ['id']
        extra_kwargs = {
            'post': {'required': True},
            'user': {'required': True}
        }