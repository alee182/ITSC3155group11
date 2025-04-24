from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.conf import settings
from django.utils.text import slugify

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='uncc-logo.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # For admin login compatibility

    def __str__(self):
        return self.email

    @property
    def full_name_slug(self):
        return slugify(f"{self.first_name} {self.last_name}")




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

#sales-listing
class Listing(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
        ('venmo', 'Venmo'),
        ('zelle', 'Zelle'),
        ('cashapp', 'CashApp'),
        ('other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('used', 'Used'),
        ('new', 'New'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(default='No description provided.')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    accepted_payments = models.CharField(max_length=100, null=True, blank=True)  # comma-separated string
    negotiable = models.BooleanField(default=False)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    created_by = models.ForeignKey('base.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def featured_image(self):
        return self.images.first().image if self.images.exists() else None


class ListingImage(models.Model):
    listing = models.ForeignKey('Listing', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')

    def __str__(self):
        return f"Image for {self.listing.title}"

class Review(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} on {self.listing.title}"


