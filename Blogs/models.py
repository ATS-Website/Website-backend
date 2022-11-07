from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    bio = models.TextField()
    profile_pics = models.ImageField(
        upload_to="media/profile_pic/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    Inactive_objects = InActiveManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

# BLOGS


class Tag(models.Model):
    name = models.CharField(max_length=15, help_text="Enter a suitable tag to help find the post",)

    def __str__(self):
        return self.name


class BlogArticle(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    intro = models.CharField(max_length=400)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # likes=models.ManyToManyField(User)

    objects = models.Manager()
    active_objects = ActiveManager()
    Inactive_objects = InActiveManager()

    class Meta:
        ordering = ['-created_at']

    # def save(self, *args, **kwargs):
    #     self.intro = self.description[:40]
    #     return super().save(*args, **kwargs)


# @receiver(pre_save, sender=BlogArticle)
# def my_callback(sender, instance, *args, **kwargs):
#     instance.intro = instance.description[:40]

    @property
    def by_tags(self):
        return [str(tag) for tag in self.tags.all]

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    blog_article = models.ForeignKey(
        BlogArticle, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment {} by {}' .format(self.name, self.description)


# NEWS

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    intro = models.CharField(max_length=400)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # likes=models.ManyToManyField(User)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.intro = self.description[:40]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class NewsComment(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    news_article = models.ForeignKey(NewsArticle, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment {} by {}' .format(self.description, self.name)


# NEWSLETTER
class NewsLetterSubscription(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class NewsLetter(models.Model):
    title =models.CharField(max_length=200)
    content= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    newslettersubscription = models.ForeignKey(NewsLetterSubscription, on_delete=models.SET_NULL, null=True)

    def send_letter(self):
        return 



# GALLERY
class Gallery(models.Model):
    image = models.ImageField()
    text = models.CharField(max_length=250, blank=True, null=True)



