from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # followers = models.ManyToManyField(User)
