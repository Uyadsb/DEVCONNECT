from django.db import models

# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=255)
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
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=folder_file_path)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_path(self):
        return self.folder.get_path() + self.name
    

class Repo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='repo_pics/%Y/%m/%d/', blank=True, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='repo_files', blank=True, null=True)
    file = models.FileField(upload_to=folder_file_path, blank=True, null=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='post_pics/%Y/%m/%d/', blank=True, null=True)
    file = models.FileField(upload_to=folder_file_path, blank=True, null=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.post.title} by {self.created_at}'
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like on {self.post.title} by {self.user}'