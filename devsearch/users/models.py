from django.db import models
from django.contrib.auth.models import User

from inherit_me.models import CreatedModifiedDateTime
import uuid


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_stackoverflow = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField('Skill', related_name='profiles')

    def __str__(self):
        return str(self.username)

class Skill(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    

class Message(CreatedModifiedDateTime):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    body = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    read_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ["is_read", "-created_at"]

