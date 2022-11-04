from django.contrib import admin
from Blogs.models import *
# Register your models here.


admin.site.register(Blog)
admin.site.register(Tags)
admin.site.register(BlogComment)
admin.site.register(Author)
admin.site.register(News)
admin.site.register(Category)
admin.site.register(NewsComment)
admin.site.register(NewsLetterSubscription)
admin.site.register(Gallery)