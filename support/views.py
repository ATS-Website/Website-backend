from rest_framework.generics import ListAPIView

from .serializers import FrequentlyAskedQuestionsSerializer, FrequentlyAskedQuestionsDetailSerializer, \
    ContactUsSerializer, ContactUsDetailSerializer
from .models import FrequentlyAskedQuestions, ContactUs
from .mixins import AdminOrReadOnlyMixin

from blogs.permissions import IsAdminOrReadOnly

from accounts.permissions import IsValidRequestAPIKey

from tech_stars.renderers import CustomRenderer
from tech_stars.mixins import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView, CustomDestroyAPIView


# Create your views here.


class FrequentlyAskedQuestionListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = FrequentlyAskedQuestions.active_objects.all()
    serializer_class = FrequentlyAskedQuestionsSerializer
    renderer_classes = (CustomRenderer,)


class FrequentlyAskedQuestionDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = FrequentlyAskedQuestions.active_objects.all()
    serializer_class = FrequentlyAskedQuestionsDetailSerializer
    renderer_classes = (CustomRenderer,)


class FrequentlyAskedQuestionListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = FrequentlyAskedQuestions.inactive_objects.all()
    serializer_class = FrequentlyAskedQuestionsSerializer


class FrequentlyAskedQuestionRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = FrequentlyAskedQuestions.inactive_objects.all()
    serializer_class = FrequentlyAskedQuestionsSerializer


class ContactUsListCreateAPIView(IsValidRequestAPIKey, CustomListCreateAPIView):
    queryset = ContactUs.active_objects.all()
    serializer_class = ContactUsSerializer
    renderer_classes = (CustomRenderer,)


class ContactUsDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = ContactUs.active_objects.all()
    serializer_class = ContactUsDetailSerializer
    renderer_classes = (CustomRenderer,)
