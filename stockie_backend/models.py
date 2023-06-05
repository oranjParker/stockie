# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_creator = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collections = models.ManyToManyField('Collection')

class MediaPost(models.Model):
    title = models.CharField(max_length=255)
    media = models.FileField(upload_to='media/')
    categories = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')

class Collection(models.Model):
    name = models.CharField(max_length=255)
    media_posts = models.ManyToManyField(MediaPost)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
