from rest_framework import serializers
from .models import File, Folder, Repo, Like, Post, Comment
from accounts.serializers import UserSerializer

        
class FolderSerializer(serializers.ModelSerializer):
    parent_name = serializers.StringRelatedField(source='parent', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True, write_only=True)
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent', 'parent_name']
        read_only_fields = ['id', 'parent_name', 'name']
        extra_kwargs = {
            'parent': {'required': False}
        }
   
class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    folder = FolderSerializer
    class Meta:
        model = File
        fields = ['id', 'name', 'folder', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'folder': {'required': True},
            'file': {'required': True}
        }     
        
class RepoSerializer(serializers.ModelSerializer):
    folder = FolderSerializer(required=False)
    file = FileSerializer(required=False)
    picture = serializers.ImageField(required=False)
    class Meta:
        model = Repo
        fields = ['id', 'title', 'content', 'picture', 'folder', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'folder': {'required': False},
            'file': {'required': False}
        }
        
        
class PostSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    file = serializers.FileField(required=False)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'picture', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'file': {'required': False}
        }
        

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'post': {'required': True},
            'content': {'required': True}
        }
        

class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']
        read_only_fields = ['id']
        extra_kwargs = {
            'post': {'required': True},
            'user': {'required': True}
        }
