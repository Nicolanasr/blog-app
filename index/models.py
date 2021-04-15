from django.db import models
from django.contrib.auth.models import User
from authentication.models import Profile


# Tags model ability to add tags to a post (tech, science ...)
class Tags(models.Model):
    tag_name = models.CharField(max_length=50, null=False, blank=False)


# Post model
class Post(models.Model):
    title = models.TextField(max_length=200, null=False, blank=False)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags)
    # TODO thumbnail = models.ImageField()


# Comments to a post model
class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL,  null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

# TODO create replies to comment
