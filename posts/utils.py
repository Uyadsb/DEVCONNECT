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