from django.contrib import admin
from .models import ContactUs, FrequentlyAskedQuestions

# Register your models here.
admin.site.register(FrequentlyAskedQuestions)
admin.site.register(ContactUs)
