from django.db import models
from django.conf import settings
from django.utils import timezone
import os

def post_image_path(instance, filename):
    # File will be uploaded to media/posts/<username>/<filename>
    return f'posts/{instance.user.username}/{filename}'

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=post_image_path)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    

# Add this to feed/models.py
class Confession(models.Model):
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='confessions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.is_anonymous:
            return f"Anonymous confession on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        return f"Confession by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes
    
    def __str__(self):
        return f"Like by {self.user.username} on {self.post}"