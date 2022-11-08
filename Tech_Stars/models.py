import datetime

from django.core.exceptions import ValidationError
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


def _json_dict():
    return dict


class TechStar(models.Model):
    tech_star_id = models.CharField(max_length=50, null=True, unique=True, editable=False)
    full_name = models.CharField(max_length=500, null=True)
    course = models.CharField(max_length=500, null=True)
    profile_picture = models.ImageField(null=True, upload_to="tech_star_picture/", blank=True)
    self_description = models.TextField(null=True)
    official_email = models.EmailField(null=True, unique=True, blank=True)
    favorite_meal = models.CharField(max_length=50)
    favorite_quote = models.TextField(null=True)
    cohort = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


class Attendance(models.Model):
    STATUS_CHOICES = (
        ("Fraudulent", "Fraudulent"),
        ("Successful", "Successful"),
        ("Uncompleted", "Uncompleted"),
    )
    tech_star = models.ForeignKey(TechStar, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15, null=True, choices=STATUS_CHOICES)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        ordering = ("-date_created",)


class Testimonial(models.Model):
    tech_star = models.ForeignKey(TechStar, on_delete=models.SET_NULL, null=True)
    testimonial = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def tech_star_full_name(self):
        return self.tech_star.full_name

    def tech_star_profile_picture(self):
        return self.tech_star.profile_picture

    def tech_star_course(self):
        return self.tech_star.course

    def tech_star_cohort(self):
        return self.tech_star.cohort


class ResumptionAndClosingTime(models.Model):
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk and ResumptionAndClosingTime.objects.exists():
            raise ValidationError("Only one instance of this object can be created !")
        return super(ResumptionAndClosingTime, self).save(*args, **kwargs)


class OfficeLocation(models.Model):
    latitude_1 = models.DecimalField(decimal_places=7, max_digits=10)
    latitude_2 = models.DecimalField(decimal_places=7, max_digits=10)
    longitude_1 = models.DecimalField(decimal_places=7, max_digits=10)
    longitude_2 = models.DecimalField(decimal_places=7, max_digits=10)

    def save(self, *args, **kwargs):
        if not self.pk and OfficeLocation.objects.exists():
            raise ValidationError("Only one instance of this object can be created !")
        return super(OfficeLocation, self).save(*args, **kwargs)


class XpertOfTheWeek(models.Model):
    tech_star = models.ForeignKey(TechStar, on_delete=models.SET_NULL, null=True)
    interview = models.JSONField(default=_json_dict())
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        ordering = ("-date_created", )
