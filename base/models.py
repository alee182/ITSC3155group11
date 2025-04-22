from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='uncc-logo.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Keep 'username' for admin

    def __str__(self):
        return self.email


# Post model for community listings
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_by = models.ForeignKey('base.User', on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


# Comments on posts
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('base.User', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


# Direct messages between users
class Message(models.Model):
    sender = models.ForeignKey('base.User', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('base.User', related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"
