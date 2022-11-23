from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
import datetime
from .utils import time_taken_to_read


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


def _json_list():
    return list


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    bio = models.TextField()
    twitter_link = models.CharField(max_length=900, null=True, blank=True)
    facebook_link = models.CharField(max_length=500, null=True, blank=True)
    instagram_link = models.CharField(max_length=500, null=True, blank=True)
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
    name = models.CharField(max_length=15, help_text="Enter a suitable tag to help find the post", )
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def __str__(self):
        return self.name


# BLOGS


class BlogArticle(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, limit_choices_to={"is_active": True})
    author = models.ForeignKey(
        Author, null=True, on_delete=models.SET_NULL, default="anonymous")
    image = models.ImageField(
        blank=True, upload_to='media/blog_article/images/', null=True)
    author = models.ForeignKey(
        Author, null=True, on_delete=models.SET_NULL, default="anonymous")

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    Inactive_objects = InActiveManager()

    class Meta:
        ordering = ['-created_at']

    def likes_count(self):
        return Likes.active_objects.filter(blog_article_id=self.id).count()

    def comment_count(self):
        return Comment.active_objects.filter(blog_article_id=self.id).count()

    def intro(self):
        return self.description[:400]

    def views_count(self):
        try:
            return len(Views.active_objects.filter(blog_article_id=self.id).first().viewer_ip)
        except:
            return 0

    def min_read(self):
        return time_taken_to_read(str(self.title), str(self.description))

    def author_fullname(self):
        return f"{self.author}"

    def few_comments(self):
        return Comment.active_objects.filter(blog_article_id=self.id)[:4]

    # def author_profile_pic(self):
    #     return self.author.profile_pics

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
    inactive_objects = InActiveManager()

    class Meta:
        ordering = ['-created_at']
        unique_together = ("name", "description", "blog_article", "is_active")

    def __str__(self):
        return 'Comment {} by {}'.format(self.name, self.description)


class Likes(models.Model):
    blog_article = models.ForeignKey(
        BlogArticle, on_delete=models.SET_NULL, null=True)
    ip_address = models.JSONField(default=_json_list())
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


class Views(models.Model):
    blog_article = models.ForeignKey(
        BlogArticle, related_name="blog_views", on_delete=models.SET_NULL, null=True)
    viewer_ip = models.JSONField(default=_json_list())
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()


# NEWS

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        unique_together = ("name", "is_active")

    def __str__(self):
        return self.name

    def category_news_count(self):
        return NewsArticle.active_objects.filter(category_id=self.id).count()

    def save(self, *args, **kwargs):
        if Category.active_objects.all().count() <= 6:
            return super(Category, self).save(*args, **kwargs)
        raise ValidationError("Categories cannot be more than 6 !")


class NewsArticle(models.Model):
    title = models.CharField(max_length=250, null=True)
    intro = models.CharField(max_length=400)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        blank=True, upload_to='media/news_article/images/', null=True, )
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def category_name(self):
        return self.category.name


class NewsComment(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    news_article = models.ForeignKey(NewsArticle, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.description, self.name)


# NEWSLETTER# NEWSLETTER


class NewsLetterSubscription(models.Model):
    email = models.EmailField(null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        unique_together = ("email", "is_active")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if NewsLetterSubscription.active_objects.filter(email=self.email).first() is not None:
            raise ValidationError("It already Exist")
        return super(NewsLetterSubscription, self).save(*args, **kwargs)


class NewsLetter(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    subject = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def __str__(self) -> str:
        return self.title

    # GALLERY


# class Gallery(models.Model):
#     image = models.ImageField(
#         blank=True, upload_to="gallery/images/", null=True)
#     # video = models.FileField(blank=True, upload_to="gallery/videos/",
#     #                          null=True, storage=VideoMediaCloudinaryStorage(),validator=[validate_])
#     text = models.CharField(max_length=250, null=True)
#     date_added = models.DateField(auto_now_add=True, null=True)
#     is_active = models.BooleanField(default=True)
#
#     objects = models.Manager()
#     active_objects = ActiveManager()
#     inactive_objects = InActiveManager()
#
#     def save(self, *args, **kwargs):
#         if self.image is None:
#             raise ValidationError(
#                 "Image cannot be empty !")
#         return super(Gallery, self).save(*args, **kwargs)


class Album(models.Model):
    name = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        unique_together = ("name", "is_active")

    def __str__(self):
        return self.name

    @property
    def active_images(self):
        return Images.active_objects.filter(album_id=self.id)


class Images(models.Model):
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_active": True}, blank=True)
    image = models.ImageField(upload_to="Tech_Stars/ATS-Gallery")
    alt = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    class Meta:
        unique_together = ("album", "image", "is_active")
