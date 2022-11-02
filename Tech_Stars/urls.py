from django.urls import path

from .views import (ProgramListCreateAPIView, ProgramRetrieveUpdateDeleteView,
                    TestimonialListCreateAPIView, TestimonialDetailUpdateDeleteView,
                    TechStarListCreateAPIView, TechStarDetailsUpdateDeleteAPIView
                    )


app_name = "Tech_Stars"

urlpatterns = [
    path("program-list-create/", ProgramListCreateAPIView.as_view(), name="program_list_create"),
    path("program-detail-update-delete/<int:pk>/", ProgramRetrieveUpdateDeleteView.as_view(), name="program_detail_update_delete"),

    path("testimonial-list-create/", TestimonialListCreateAPIView.as_view(), name="testimonial_list_create"),
    path("testimonial-detail-update-delete/<int:pk>/", TestimonialDetailUpdateDeleteView.as_view(), name="testimonial_detail_update_delete"),

    path("tech-star-list-create/", TechStarListCreateAPIView.as_view(), name="tech_star_list_create"),
    path("tech-star-details-update-delete/<int:pk>/", TechStarDetailsUpdateDeleteAPIView.as_view(), name="tech_star_details_update_delete"),

]
