from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from .serializers import FrequentlyAskedQuestionsSerializer, FrequentlyAskedQuestionsDetailSerializer, ContactUsSerializer, ContactUsDetailSerializer
from .models import FrequentlyAskedQuestions, ContactUs
from Tech_Stars.renderers import CustomRenderer
from Tech_Stars.permissions import IsAdminOrReadOnly
from Tech_Stars.mixins import AdminOrReadOnlyMixin

# Create your views here.


class FrequentlyAskedQuestionListCreateAPIView(AdminOrReadOnlyMixin, ListCreateAPIView):
    queryset = FrequentlyAskedQuestions.active_objects.all()
    serializer_class = FrequentlyAskedQuestionsSerializer
    renderer_classes = (CustomRenderer,)


class FrequentlyAskedQuestionDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, RetrieveUpdateDestroyAPIView):
    queryset = FrequentlyAskedQuestions.active_objects.all()
    serializer_class = FrequentlyAskedQuestionsDetailSerializer
    renderer_classes = (CustomRenderer,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


class ContactUsListCreateAPIView(AdminOrReadOnlyMixin, ListCreateAPIView):
    queryset = ContactUs.active_objects.all()
    serializer_class = ContactUsSerializer
    renderer_classes = (CustomRenderer, )


class ContactUsDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.active_objects.all()
    serializer_class = ContactUsDetailSerializer
    renderer_classes = (CustomRenderer, )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)

