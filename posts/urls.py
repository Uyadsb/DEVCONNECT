from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import LikePostView, CommentView, FileView, PostView, RepoView, FolderView

DefaultRouter = DefaultRouter()
DefaultRouter.register(r'files', FileView, basename='file')
DefaultRouter.register(r'posts', PostView, basename='post')
DefaultRouter.register(r'repos', RepoView, basename='repo')
DefaultRouter.register(r'folders', FolderView, basename='folder')
DefaultRouter.register(r'likes', LikePostView, basename='like')
DefaultRouter.register(r'comments', CommentView, basename='comment')

urlpatterns = []
urlpatterns += DefaultRouter.urls