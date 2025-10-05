from django.db import models

# Create your models here.

    
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_path(self):
        return self.folder.get_path() + self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='post_pics/%Y/%m/%d/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

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