from django.shortcuts import render
from .models import File, Folder, Repo
from .serialisers import FileSerializer, FolderSerializer, RepoSerializer
from rest_framework import viewsets, permissions

# Create your views here.
class RepoView(MultiFileUploadMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RepoSerializer
    queryset = Repo.objects.all()
    
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
    
class FileView(MultiFileUploadMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer
    queryset = File.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request):
        # Handle multiple file uploads
        return self.handle_multi_file_upload(request, self.serializer_class, extra_data={'user': request.user})
    