from django.contrib import admin
from Blogs.models import *
# Register your models here.


admin.site.register(BlogArticle)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(NewsArticle)
admin.site.register(Category)
admin.site.register(NewsComment)
admin.site.register(NewsLetterSubscription)
admin.site.register(Gallery)
admin.site.register(NewsLetter)