from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='reports/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models

from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    about = models.TextField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
