import datetime

from django.db import models


# Create your models here.

class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


first = f"{datetime.datetime.today().year}"
second = f"{(datetime.datetime.today() + datetime.timedelta(days=365)).year}"


class Program(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


class TechStar(models.Model):
    YEAR_CHOICES = (
        (first, first),
        (second, second)
    )
    user = models.ForeignKey("Accounts.Accounts", on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(null=True, upload_to="tech_star_picture/")
    self_description = models.TextField(null=True)
    favorite_meal = models.CharField(max_length=50)
    favorite_quote = models.TextField(null=True)
    year = models.CharField(max_length=15, null=True, choices=YEAR_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


