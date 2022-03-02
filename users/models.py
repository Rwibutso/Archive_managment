from signal import signal
from django.db import models
# from django.contrib.auth import user
from django.dispatch import receiver

# class UserProfile(models.Model):
#     profile_user = models.OneToOneField(user, om_delete=CASCADE)
#     profile_img = models.ImageField(upload_to="file")


# @receiver(post_save, sender=user)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.abjects.create(profile_user=instance)
#         instance.userprofile.save
