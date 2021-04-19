from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from authentication.models import Profile


# Tags model ability to add tags to a post (tech, science ...)
class Tags(models.Model):
    def __str__(self):
        return self.tag_name
    tag_name = models.CharField(max_length=50, null=False, blank=False)


# Post model
class Post(models.Model):
    def __str__(self):
        return self.title
    title = models.TextField(max_length=200, null=False, blank=False)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags)
    thumbnail = models.URLField(null=False, blank=False)


# To check if a user has already likes a post
class LikesUsers(models.Model):
    def __str__(self):
        if self.value == 1:
            return f'{self.post}-{self.user.user.username}-like'
        elif self.value == -1:
            return f'{self.post}-{self.user.user.username}-dislike'

    choice = (
        (1, "like"),
        (-1, "dislike"),
    )
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    value = models.IntegerField(choices=choice, null=False, blank=False)


# Comments to a post model
class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL,  null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

# TODO create replies to comment


# Signal to create an instance Profile when a User is create
def create_profile(sender, instance, created, **kwargs):
    user = User.objects.get(username=instance)
    profile = Profile(user=user)
    profile.save()


post_save.connect(create_profile, sender=User)
