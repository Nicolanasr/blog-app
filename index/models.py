from django.db import models
from django.contrib.auth.models import User

from authentication.models import Profile


# Tags model ability to add tags to a post (tech, science ...)
class Tags(models.Model):
    def __str__(self):
        return self.tag_name
    tag_name = models.CharField(max_length=50, null=False, blank=False)


# Post model
class Post(models.Model):
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    title = models.TextField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    views_for_algo = models.IntegerField(default=0) # To hide from admin: , db_index=True, editable=False
    rank = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tags)
    thumbnail = models.URLField(null=True, blank=True)
    shared = models.BooleanField(default=False)
    shared_by = models.ForeignKey(Profile, related_name="shared_by", on_delete=models.SET_NULL, null=True, blank=True)
    shared_post_id = models.IntegerField(null=True, blank=True)
    shared_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


# To check if a user has already likes a post
class LikesUsers(models.Model):
    def __str__(self):
        try:
            if self.value == 1:
                return f'{self.post}-{self.user.user.username}-like'
            elif self.value == -1:
                return f'{self.post}-{self.user.user.username}-dislike'
        except:
            if self.value == 1:
                return 'User deleted-like'
            elif self.value == -1:
                return 'User deleted-dislike'

    choice = (
        (1, "like"),
        (-1, "dislike"),
    )
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    value = models.IntegerField(choices=choice, null=False, blank=False)


class ViewedPost(models.Model):
    def __str__(self):
        return str(self.Profile) + "-" + str(self.post)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

# Comments to a post model
class Comments(models.Model):
    class Meta:
        ordering = ['-created_at']
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL,  null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

# TODO create replies to comment

