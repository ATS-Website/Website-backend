from django.urls import path
from rest_framework import routers


from .views import (
    TestimonialListCreateAPIView, TestimonialDetailUpdateDeleteView,
    TechStarListCreateAPIView, TechStarDetailsUpdateDeleteAPIView,
    GenerateAttendanceQRCode, ResumptionAndClosingTimeCreateAPIView,
    ResumptionAndClosingTimeDetailsUpdateDetailAPIView, RecordAttendanceAPIView,
    AttendanceListAPIView, OfficeLocationCreateAPIView, OfficeLocationDetailsUpdateAPIView,
    TestimonialFrontpageListAPIView, XpertOfTheWeekListCreateAPIView, XpertOfTheWeekDetailUpdateDeleteAPIView,
    ReadAdminLog, WriteAdminLog, TrashedTechStarListAPIView, TrashedTechStarRestoreAPIView, TrashedTestimonialListAPIView,
    TrashedTestimonialRestoreAPIView, TrashedXpertListAPIView, TrashedXpertRestoreAPIView, TechStarDocumentView, RecentXpertOfTheWeekAPIView
)


app_name = "tech_stars"
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'techstar-search', TechStarDocumentView,
                basename='techstar-search')

urlpatterns = [
    path("testimonial-list-create/", TestimonialListCreateAPIView.as_view(),
         name="testimonial_list_create"),
    path("testimonial-detail-update-delete/<int:pk>/",
         TestimonialDetailUpdateDeleteView.as_view(), name="testimonial_detail_update_delete"),
    path("testimonial-frontpage-list/", TestimonialFrontpageListAPIView.as_view(),
         name="testimonial_frontpage_list"),
    path('testimonial-trash', TrashedTestimonialListAPIView.as_view(),
         name="testimonial_trash"),
    path('testimonial-trash-restore/<int:pk>',
         TrashedTestimonialRestoreAPIView.as_view(), name="testimonial_trash_restore"),

    path("tech-star-list-create/", TechStarListCreateAPIView.as_view(),
         name="tech_star_list_create"),
    path("tech-star-details-update-delete/<int:pk>/",
         TechStarDetailsUpdateDeleteAPIView.as_view(), name="tech_star_details_update_delete"),
    path('tech-star-trash', TrashedTechStarListAPIView.as_view(),
         name="tech_star_trash"),
    path('tech-star-trash-restore/<int:pk>',
         TrashedTechStarRestoreAPIView.as_view(), name="tech_star_trash_restore"),

    path("resumption-closing-time-create/", ResumptionAndClosingTimeCreateAPIView.as_view(),
         name="resumption_closing_time_create"),
    path("resumption-closing-time-detail-update/", ResumptionAndClosingTimeDetailsUpdateDetailAPIView.as_view(),
         name="resumption_closing_time_details_update"),

    path("QR-code-generator/", GenerateAttendanceQRCode.as_view(),
         name="qr_code_generator"),
    path("record-attendance/", RecordAttendanceAPIView.as_view(),
         name="record_attendance"),
    path("attendance-list/", AttendanceListAPIView.as_view(), name="attendance_list"),

    path("office-location-create/", OfficeLocationCreateAPIView.as_view(),
         name="office_location_create"),
    path("office-location-detail-update/", OfficeLocationDetailsUpdateAPIView.as_view(),
         name="office_location_detail_update"),


    path("Xpert-Of-the-week-list-create/",
         XpertOfTheWeekListCreateAPIView.as_view(), name="xpert_list_create"),
    path("Xpert-of-the-week-detail-update-destroy/<int:pk>/",
         XpertOfTheWeekDetailUpdateDeleteAPIView.as_view(), name="xpert_detail_update_delete"),
    path('xpert-trash', TrashedXpertListAPIView.as_view(), name="xpert_trash"),
    path('xpert-trash-restore/<int:pk>',
         TrashedXpertRestoreAPIView.as_view(), name="xpert_trash_restore"),

    path("recent-xpert-of-the-week/", RecentXpertOfTheWeekAPIView.as_view(), name="recent_xpert_of_the_week"),

    path("read-admin-log/", ReadAdminLog.as_view(), name="read_admin_log"),
    path("write-admin-log/", WriteAdminLog.as_view(), name="write_admin_log")



]

urlpatterns += router.urls
