import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from Accounts.models import Account


# Create your models here.

class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


zero = f"{(datetime.datetime.today() - datetime.timedelta(days=365)).year}"
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
        (zero, zero),
        (first, first),
        (second, second),
    )
    tech_star_id = models.CharField(max_length=50, null=True, unique=True)
    full_name = models.CharField(max_length=500, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(null=True, upload_to="tech_star_picture/", blank=True)
    self_description = models.TextField(null=True)
    official_email = models.EmailField(null=True, unique=True, blank=True)
    favorite_meal = models.CharField(max_length=50)
    favorite_quote = models.TextField(null=True)
    year = models.CharField(max_length=15, null=True, choices=YEAR_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


#
# class Attendance(models.Model):
#     STATUS_CHOICES = (
#         ("Fraudulent", "Fraudulent"),
#         ("Successful", "Successful")
#     )
#     user = models.ForeignKey(TechStar, on_delete=models.SET_NULL, null=True)
#     check_in = models.DateTimeField()
#     check_out = models.DateTimeField()
#     location = models.CharField(max_length=300, null=True)

class Testimonial(models.Model):
    tech_star = models.ForeignKey(TechStar, on_delete=models.SET_NULL, null=True)
    testimonial = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


# def id_creator_checker(number: int):
#     get_id = number + 1
#     id2string = str(get_id).zfill(4)
#     return id2string


@receiver(post_save, sender=TechStar)
def set_tech_star_id(sender, instance, created, **kwargs):
    if created:
        tech_star = TechStar.objects.all().last()

        if tech_star is not None:
            get_id = int(tech_star.tech_star_id[-4::]) + 1
            instance.tech_star_id = f"ATS-{str(get_id).zfill(4)}"
            instance.save()

        else:
            instance.tech_star_id = f"ATS-0001"
            instance.save()
