from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
import zipfile

from .models import File, Folder, Repo
from .serialisers import FileSerializer, FolderSerializer, RepoSerializer


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
        # Handle multiple file uploads for repo creation
        return self.handle_multi_file_upload(request, self.serializer_class, extra_data={'user': request.user})


class FolderView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload-zip')
    def upload_zip(self, request):
        """
        Upload a ZIP file and extract its structure into folders and files.
        Expected: 'zip_file' in request.FILES
        Optional: 'parent_folder_id' to specify where to extract
        """
        zip_file = request.FILES.get('zip_file')
        parent_folder_id = request.data.get('parent_folder_id')

        if not zip_file:
            return Response({"detail": "No ZIP file provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not zip_file.name.endswith('.zip'):
            return Response({"detail": "File must be a ZIP archive."}, status=status.HTTP_400_BAD_REQUEST)

        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id, user=request.user)

        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                folder_cache = {}  # {path: Folder instance}
                created_folders = []
                created_files = []

                file_list = zip_ref.namelist()
                for file_path in file_list:
                    if file_path.endswith('/'):
                        # Skip directories from ZIP (they'll be created as needed)
                        continue
                    path_parts = file_path.split('/')
                    filename = path_parts[-1]
                    dir_parts = path_parts[:-1]

                    current_parent = parent_folder
                    current_path = ""
                    for folder_name in dir_parts:
                        current_path += folder_name + "/"
                        if current_path not in folder_cache:
                            existing_folder = Folder.objects.filter(
                                name=folder_name,
                                parent=current_parent,
                                user=request.user
                            ).first()
                            if existing_folder:
                                folder_cache[current_path] = existing_folder
                            else:
                                new_folder = Folder.objects.create(
                                    name=folder_name,
                                    parent=current_parent,
                                    user=request.user
                                )
                                folder_cache[current_path] = new_folder
                                created_folders.append(new_folder)
                        current_parent = folder_cache[current_path]

                    if current_parent:
                        file_content = zip_ref.read(file_path)
                        django_file = ContentFile(file_content, name=filename)
                        new_file = File.objects.create(
                            name=filename,
                            folder=current_parent,
                            user=request.user,
                            file=django_file
                        )
                        created_files.append(new_file)

                return Response({
                    "message": "ZIP extracted successfully",
                    "created_folders": len(created_folders),
                    "created_files": len(created_files),
                    "folders": FolderSerializer(created_folders, many=True).data,
                    "files": FileSerializer(created_files, many=True).data
                }, status=status.HTTP_201_CREATED)

        except zipfile.BadZipFile:
            return Response({"detail": "Invalid ZIP file."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error extracting ZIP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='upload-with-structure')
    def upload_with_structure(self, request):
        """
        Upload multiple files with their relative paths.
        Expected format:
        - files[]: multiple files
        - paths[]: corresponding paths (e.g., 'src/components/Header.js')
        Optional:
        - parent_folder_id: root folder ID
        """
        files = request.FILES.getlist('files')
        paths = request.data.getlist('paths')
        parent_folder_id = request.data.get('parent_folder_id')

        if not files:
            return Response({"detail": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

        if len(files) != len(paths):
            return Response({"detail": "Number of files must match number of paths."}, status=status.HTTP_400_BAD_REQUEST)

        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id, user=request.user)

        try:
            folder_cache = {}  # {path: Folder instance}
            created_folders = []
            created_files = []

            for file, relative_path in zip(files, paths):
                relative_path = relative_path.replace('\\', '/')
                path_parts = relative_path.split('/')
                filename = path_parts[-1]
                dir_parts = path_parts[:-1]

                current_parent = parent_folder
                current_path = ""
                for folder_name in dir_parts:
                    current_path += folder_name + "/"
                    if current_path not in folder_cache:
                        existing_folder = Folder.objects.filter(
                            name=folder_name,
                            parent=current_parent,
                            user=request.user
                        ).first()
                        if existing_folder:
                            folder_cache[current_path] = existing_folder
                        else:
                            new_folder = Folder.objects.create(
                                name=folder_name,
                                parent=current_parent,
                                user=request.user
                            )
                            folder_cache[current_path] = new_folder
                            created_folders.append(new_folder)
                    current_parent = folder_cache[current_path]

                if current_parent:
                    new_file = File.objects.create(
                        name=filename,
                        folder=current_parent,
                        user=request.user,
                        file=file
                    )
                    created_files.append(new_file)
                else:
                    return Response({"detail": f"Cannot create file '{filename}' without a folder."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Files uploaded successfully with structure",
                "created_folders": len(created_folders),
                "created_files": len(created_files),
                "folders": FolderSerializer(created_folders, many=True).data,
                "files": FileSerializer(created_files, many=True).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": f"Error uploading files: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileView(MultiFileUploadMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        # Handle multiple file uploads
        return self.handle_multi_file_upload(request, self.serializer_class, extra_data={'user': request.user})
