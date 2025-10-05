from rest_framework import views
from rest_framework import viewsets

from .serialisers import (
    FileSerializer,
    FolderSerializer,
    RepoSerializer,
    LikeSerializer,
    PostSerializer,
    CommentSerializer
)
from rest_framework import permissions, status
from .models import File, Folder, Repo, Like, Post, Comment
from rest_framework.response import Response
from .utils import MultiFileUploadMixin

class LikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get(self, request, post_id=None):
        # Fetch all likes, or likes for a specific post if post_id is provided
        post_id_param = post_id or request.query_params.get('post_id')
        queryset = Like.objects.all()
        if post_id_param:
            queryset = queryset.filter(post_id=post_id_param)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        # Check if the user already liked the post
        if Like.objects.filter(post_id=post_id, user=request.user).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new like
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(post_id=post_id, user=request.user)  # Save with post_id and user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        # Delete a like (unlike the post)
        try:
            like = Like.objects.get(post_id=post_id, user=request.user)
            like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "Like does not exist."}, status=status.HTTP_404_NOT_FOUND)


class FileView(MultiFileUploadMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer
    queryset = File.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request):
        # Handle multiple file uploads
        return self.handle_multi_file_upload(request, self.serializer_class, extra_data={'user': request.user})
    
class FolderView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

class PostView(MultiFileUploadMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset  # Return all posts if no user_id
    
    def create(self, request):
        # Handle multiple file uploads
        return self.handle_multi_file_upload(request, self.serializer_class, extra_data={'user': request.user})
    
class CommentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        user_id = self.request.query_params.get('user_id')
        queryset = self.queryset
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset  # Filter by post_id and/or user_id if provided
    
    def perform_create(self, serializer):
        # Automatically set the user to the current authenticated user
        serializer.save(user=self.request.user)