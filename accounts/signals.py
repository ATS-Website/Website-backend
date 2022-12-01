from .models import Profile, Account
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

#
# @receiver(post_save, sender=Account)
# def create_profile(sender, instance, created, **kwargs):
#     if instance and created:
#         user_profile = Profile.objects.create(account=instance)
#         instance.profile = user_profile
#         user_profile.save()
#     else:
#         try:
#             user_profile = Profile.objects.get(account=instance)
#             user_profile.save()
#         except:
#             Profile.objects.create(account=instance)
