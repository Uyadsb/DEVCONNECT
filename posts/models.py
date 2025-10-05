from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='post_pics/%Y/%m/%d/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.post.title} by {self.user.username}'
    
    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like on {self.post.title} by {self.user.username}'
    
    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes
        ordering = ['-created_at']