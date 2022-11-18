from django.contrib import admin
from .models import TechStar, Testimonial, XpertOfTheWeek, ResumptionAndClosingTime, OfficeLocation, Attendance

# Register your models here.

admin.site.register(TechStar)
admin.site.register(Testimonial)
admin.site.register(XpertOfTheWeek)
admin.site.register(ResumptionAndClosingTime)
admin.site.register(OfficeLocation)
admin.site.register(Attendance)
