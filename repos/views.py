from django.shortcuts import render
from .models import File, Folder, Repo
from .serialisers import FileSerializer, FolderSerializer, RepoSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status


class MultiFileUploadMixin:
    def handle_multi_file_upload(self, request, serializer_class, extra_data=None):
        files = request.FILES.getlist('files')
        if not files:
            return Response({"detail": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)
        data = []
        for file in files:
            file_data = request.data.copy()
            file_data['file'] = file
            if extra_data:
                file_data.update(extra_data)
            serializer = serializer_class(data=file_data)
            if serializer.is_valid():
                serializer.save()
                data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


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