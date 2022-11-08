from django.urls import path

from .views import (
                    TestimonialListCreateAPIView, TestimonialDetailUpdateDeleteView,
                    TechStarListCreateAPIView, TechStarDetailsUpdateDeleteAPIView,
                    GenerateAttendanceQRCode, ResumptionAndClosingTimeCreateAPIView,
                    ResumptionAndClosingTimeDetailsUpdateDetailAPIView, RecordAttendanceAPIView,
                    AttendanceListAPIView, OfficeLocationCreateAPIView, OfficeLocationDetailsUpdateAPIView,
                    TestimonialFrontpageListAPIView
                    )


app_name = "Tech_Stars"

urlpatterns = [
    path("testimonial-list-create/", TestimonialListCreateAPIView.as_view(), name="testimonial_list_create"),
    path("testimonial-detail-update-delete/<int:pk>/", TestimonialDetailUpdateDeleteView.as_view(), name="testimonial_detail_update_delete"),
    path("testimonial-frontpage-list/", TestimonialFrontpageListAPIView.as_view(), name="testimonial_frontpage_list"),

    path("tech-star-list-create/", TechStarListCreateAPIView.as_view(), name="tech_star_list_create"),
    path("tech-star-details-update-delete/<int:pk>/", TechStarDetailsUpdateDeleteAPIView.as_view(), name="tech_star_details_update_delete"),

    path("resumption-closing-time-create/", ResumptionAndClosingTimeCreateAPIView.as_view(), name="resumption_closing_time_create"),
    path("resumption-closing-time-detail-update/", ResumptionAndClosingTimeDetailsUpdateDetailAPIView.as_view(), name="resumption_closing_time_details_update"),

    path("QR-code-generator/", GenerateAttendanceQRCode.as_view(), name="qr_code_generator"),
    path("record-attendance/", RecordAttendanceAPIView.as_view(), name="record_attendance"),
    path("attendance-list/", AttendanceListAPIView.as_view(), name="attendance_list"),

    path("office-location-create/", OfficeLocationCreateAPIView.as_view(), name="office_location_create"),
    path("office-location-detail-update/", OfficeLocationDetailsUpdateAPIView.as_view(), name="office_location_detail_update"),



]
