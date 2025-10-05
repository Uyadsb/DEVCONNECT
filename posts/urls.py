from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikePostView, CommentView, FileView, PostView, RepoView, FolderView

router = DefaultRouter()
# Register all ViewSets with the router
router.register(r'files', FileView, basename='file')
router.register(r'posts', PostView, basename='post')
router.register(r'comments', CommentView, basename='comment')

urlpatterns = [
    # APIView routes for LikePostView (keep this as APIView)
    path('likes/', LikePostView.as_view(), name='like-list'),
    path('likes/<int:post_id>/', LikePostView.as_view(), name='like-detail'),
]

# Add router URLs
urlpatterns += router.urls