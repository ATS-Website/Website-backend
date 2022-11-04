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
   first_name= models.CharField(max_length= 100)
   last_name=models.CharField(max_length=200)
   email= models.EmailField()
   author_bio= models.TextField()
   author_profile_pics= models.ImageField(upload_to="author_profile_pic/", blank=True, null=True)
   is_active = models.BooleanField(default=True)

   objects = models.Manager()
   active_objects = ActiveManager()
   Inactive_objects = InActiveManager()

   def __str__(self):
      return self.first_name + " " + self.last_name

# BLOGS

class Tags(models.Model):
   name_of_tags = models.CharField(max_length=15, 
      help_text="Enter a suitable tag to help find the post",)

   def __str__(self):
      return self.name_of_tags 


class Blog(models.Model):
   blog_title= models.CharField(max_length= 250, blank=False, null=False)
   blog_intro = models.CharField(max_length=400)
   blog_description= models.TextField()
   created_at= models.DateTimeField(auto_now_add=True)
   updated_at=models.DateTimeField(auto_now=True)
   tags = models.ManyToManyField(Tags, default=["news", "entertainment"])
   author= models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
   image=models.ImageField(blank=True, null=True)
   is_active=models.BooleanField(default=True)
   # likes=models.ManyToManyField(User)

   objects = models.Manager()
   active_objects = ActiveManager()
   Inactive_objects = InActiveManager()
   

   class Meta:
      ordering=['-created_at']

   def __str__(self):
      return self.title



class BlogComment(models.Model):
   commenter_name= models.CharField(max_length= 100, blank=False, null=False)
   your_comment= models.TextField()
   article=models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
   created_at=models.DateTimeField(auto_now_add=True)
   is_active=models.BooleanField(default=True)

   objects = models.Manager()
   active_objects = ActiveManager()

   class Meta:
      ordering=['-created_at']

   def __str__(self):
      return 'Comment {} by {}' .format(self.your_comment, self.commenter_name)


# NEWS

class Category(models.Model):
   category_name=models.CharField(max_length=100)

   def __str__(self):
      return self.category_name

   def category_news(self):
      return News.active_objects.filter(category_id=self.id)

class News(models.Model):
   news_title= models.CharField(max_length= 250, blank=False, null=False)
   news_intro = models.CharField(max_length=400)
   news_description= models.TextField()
   created_at= models.DateTimeField(auto_now_add=True)
   updated_at=models.DateTimeField(auto_now=True)
   category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
   author= models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
   image=models.ImageField(blank=True, null=True)
   is_active=models.BooleanField(default=True)
   # likes=models.ManyToManyField(User)

   objects = models.Manager()
   active_objects = ActiveManager()
   inactive_objects = InActiveManager()

   class Meta:
      ordering=['-created_at']

   def __str__(self):
      return self.title

   
class NewsComment(models.Model):
   commenter_name= models.CharField(max_length= 100, blank=False, null=False)
   your_comment= models.CharField(max_length= 100, blank=False, null=False)
   news=models.ForeignKey(News, on_delete=models.SET_NULL, null=True)
   created_at=models.DateTimeField(auto_now_add=True)
   is_active=models.BooleanField(default=True)

   objects = models.Manager()
   active_objects = ActiveManager()

   class Meta:
      ordering=['-created_at']

   def __str__(self):
      return 'Comment {} by {}' .format(self.your_comment, self.commenter_name)


# NEWSLETTER
class NewsLetterSubscription(models.Model):
   email=models.EmailField(models.Model)

   def __str__(self):
      return self.email

# GALLERY
class Gallery(models.Model):
   images= models.ImageField()
   text= models.CharField(max_length=250, blank=True, null=True)