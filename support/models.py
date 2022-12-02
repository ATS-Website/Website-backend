from django.db import models

# Create your models here.
from rest_framework.exceptions import ValidationError

from tech_stars.models import ActiveManager, InActiveManager


class FrequentlyAskedQuestions(models.Model):
    question = models.TextField(null=True, unique=True)
    answer = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def save(self, *args, **kwargs):
        if FrequentlyAskedQuestions.active_objects.all().count() >= 3:
            raise ValidationError("Faq instances cannot be more than 3")
        return super(FrequentlyAskedQuestions, self).save(*args, **kwargs)


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    subject = models.CharField(max_length=500, null=True)
    message = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def short_message(self):
        if self.message is not None:
            return self.message[:30]
        return ""
