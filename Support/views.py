from .serializers import FrequentlyAskedQuestionsSerializer, FrequentlyAskedQuestionsDetailSerializer, \
    ContactUsSerializer, ContactUsDetailSerializer
from .models import FrequentlyAskedQuestions, ContactUs
from .mixins import AdminOrReadOnlyMixin
from Tech_Stars.renderers import CustomRenderer
from Tech_Stars.mixins import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView


# Create your views here.


class FrequentlyAskedQuestionListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = FrequentlyAskedQuestions.active_objects.all()
    serializer_class = FrequentlyAskedQuestionsSerializer
    renderer_classes = (CustomRenderer,)


class FrequentlyAskedQuestionDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = FrequentlyAskedQuestions.active_objects.all()
    serializer_class = FrequentlyAskedQuestionsDetailSerializer
    renderer_classes = (CustomRenderer,)


class ContactUsListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = ContactUs.active_objects.all()
    serializer_class = ContactUsSerializer
    renderer_classes = (CustomRenderer,)


class ContactUsDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = ContactUs.active_objects.all()
    serializer_class = ContactUsDetailSerializer
    renderer_classes = (CustomRenderer,)

