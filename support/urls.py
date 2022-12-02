from django.urls import path

from .views import (FrequentlyAskedQuestionListCreateAPIView, FrequentlyAskedQuestionDetailsUpdateDeleteAPIView,
                    ContactUsDetailsUpdateDeleteAPIView, ContactUsListCreateAPIView, FrequentlyAskedQuestionListAPIView,
                    FrequentlyAskedQuestionRestoreAPIView,
                    )


app_name = "support"

urlpatterns = [
    path("FAQ-list-create/", FrequentlyAskedQuestionListCreateAPIView.as_view(), name="faq_list_create"),
    path("FAQ-trash/", FrequentlyAskedQuestionListAPIView.as_view(), name="faq_trash"),
    path("FAQ-trash-restore/<int:pk>/", FrequentlyAskedQuestionRestoreAPIView.as_view(), name="faq_trash_restore"),
    path("FAQ-details-update-delete/<int:pk>/", FrequentlyAskedQuestionDetailsUpdateDeleteAPIView.as_view(), name="faq_details_update_delete"),
    path("contact-us-list-create/", ContactUsListCreateAPIView.as_view(), name="contact_us_list_create"),
    path("contact-us-details-update-delete/<int:pk>/", ContactUsDetailsUpdateDeleteAPIView.as_view(), name="contact_us_details_update_delete")
]