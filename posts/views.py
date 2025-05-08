from rest_framework import views
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


class LikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def get(self, request, post_id):
        # Fetch all likes of the post
        likes = Like.objects.filter(post_id=post_id)
        serializer = self.serializer_class(likes, many=True)
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
