from rest_framework import serializers
from .models import File, Folder, Repo, Like, Post, Comment


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'folder', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'folder': {'required': True},
            'file': {'required': True}
        }

        
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent']
        read_only_fields = ['id']
        extra_kwargs = {
            'parent': {'required': False}
        }
        
        
class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'picture', 'folder', 'file']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'folder': {'required': False},
            'file': {'required': False}
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
        
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'picture', 'file']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'file': {'required': False}
        }
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'post': {'required': True},
            'content': {'required': True}
        }