from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


