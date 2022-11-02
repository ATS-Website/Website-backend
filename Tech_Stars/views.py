from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .permissions import IsAdminOrReadOnly
from .serializers import (ProgramSerializer, ProgramDetailSerializer,
                          TestimonialSerializer, TestimonialDetailSerializer,
                          TechStarSerializer, TechStarDetailSerializer
                          )
from .renderers import CustomRenderer
from .models import Program, Testimonial, TechStar
from .mixins import AdminOrReadOnlyMixin


# Create your views here.


class ProgramListCreateAPIView(AdminOrReadOnlyMixin, ListCreateAPIView):
    serializer_class = ProgramSerializer
    renderer_classes = (CustomRenderer,)
    queryset = Program.active_objects.all()


class ProgramRetrieveUpdateDeleteView(AdminOrReadOnlyMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ProgramDetailSerializer
    renderer_classes = (CustomRenderer,)
    queryset = Program.active_objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


class TechStarListCreateAPIView(AdminOrReadOnlyMixin, ListCreateAPIView):
    serializer_class = TechStarSerializer
    queryset = TechStar.active_objects.all()
    renderer_classes = (CustomRenderer,)


class TechStarDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TechStarDetailSerializer
    queryset = TechStar.active_objects.all()
    renderer_classes = (CustomRenderer,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        return super().delete(request, *args, **kwargs)


class TestimonialListCreateAPIView(AdminOrReadOnlyMixin, ListCreateAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.active_objects.all()
    renderer_classes = (CustomRenderer,)


class TestimonialDetailUpdateDeleteView(AdminOrReadOnlyMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TestimonialDetailSerializer
    queryset = Testimonial.active_objects.all()
    renderer_classes = (CustomRenderer,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        return super().delete(request, *args, **kwargs)
