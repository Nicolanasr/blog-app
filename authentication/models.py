from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
class FollowModel(models.Model):
    def __str__(self):
        return self.follower.user.username
    
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE)
    following = models.ManyToManyField(Profile, related_name="following_list", blank=True)
    followers = models.ManyToManyField(Profile, related_name="followers_list", blank=True)



# Signal to create an instance Profile when a User is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(username=instance)
        profile = Profile(user=user)
        profile.save()
        follow_model = FollowModel(follower=profile)
        follow_model.save()
        follow_model.following.add(profile)
        follow_model.followers.add(profile)


post_save.connect(create_profile, sender=User)
