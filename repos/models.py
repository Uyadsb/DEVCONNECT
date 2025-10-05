from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repo_folders')  # Changed
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='subfolders'
    )

    def __str__(self):
        return self.name

    def get_path(self):
        """Get full path like 'src/components/'"""
        if self.parent:
            return self.parent.get_path() + self.name + '/'
        return self.name + '/'
    

def folder_file_path(instance, filename):
    return f'files/{instance.folder.get_path()}{filename}'


class File(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repo_files')  # Add this
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=folder_file_path)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_path(self):
        return self.folder.get_path() + self.name
    

class Repo(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repos')  # Add this
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='repo_pics/%Y/%m/%d/', blank=True, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='repo_items', blank=True, null=True)  # Changed related_name
    file = models.FileField(upload_to=folder_file_path, blank=True, null=True)

    def __str__(self):
        return self.title