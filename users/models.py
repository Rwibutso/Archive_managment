from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver




class UserProfile(models.Model):
    profile_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="images/", default='images/profile.jpg')
    bio = models.CharField(max_length=40)

# @receiver(post_save, sender=get_user_model)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(profile_user=instance):
#     instance.userprofile.save()        