from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepoView, FolderView


router = DefaultRouter()
# Register all ViewSets with the router

router.register(r'repos', RepoView, basename='repo')
router.register(r'folders', FolderView, basename='folder')

urlpatterns = [
    path('', include(router.urls)), # Include router URLs  
]