from django.db import models

# Create your models here.


from Tech_Stars.models import ActiveManager, InActiveManager


class FrequentlyAskedQuestions(models.Model):
    question = models.TextField(null=True)
    answer = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()
