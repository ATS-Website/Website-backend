import csv
import json
import random
from ast import literal_eval

from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import CompoundSearchFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from decouple import config

from .documents import TechStarDocument
from .serializers import (
    TestimonialSerializer, TestimonialDetailSerializer,
    TechStarSerializer, TechStarDetailSerializer,
    BarcodeSerializer, ResumptionAndClosingTimeSerializer, AttendanceSerializer,
    OfficeLocationSerializer, TestimonialFrontpageSerializer, XpertOfTheWeekSerializer,
    XpertOfTheWeekDetailSerializer, TechStarDocumentSerializer
)
from .models import Testimonial, TechStar, ResumptionAndClosingTime, Attendance, OfficeLocation, XpertOfTheWeek
from .mixins import (AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView,
                     CustomRetrieveUpdateDestroyAPIView, CustomCreateAPIView,
                     CustomRetrieveUpdateAPIView, CustomDestroyAPIView
                     )
from .utils import generate_qr
from .tasks import write_log_csv
from .enc_dec.encryption_decryption import aes_encrypt

from accounts.mixins import IsAdminOrReadOnlyMixin
from accounts.permissions import IsValidRequestAPIKey

from blogs.permissions import IsAdminOrReadOnly

# Create your views here.


# timezone.activate(settings.TIME_ZONE)

valid_days = list(range(1, 6))
time_check = ResumptionAndClosingTime.objects.all().first()
office_location = OfficeLocation.objects.all().first()


# time_check = ""
# office_location = ""
class TechStarDocumentView(DocumentViewSet):
    document = TechStarDocument
    serializer_class = TechStarDocumentSerializer

    filter_backends = [CompoundSearchFilterBackend, SuggesterFilterBackend]
    search_fields = ('full_name', "self_description",)
    suggester_fields = {
        'full_name': {
            'field': 'full_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'self_description': {
            'field': 'self_description.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
    ordering = ('-id', 'full_name', '-date_created')


def create_attendance(tech_star, date_time, device_id):
    attendance = Attendance.active_objects.create(
        tech_star=tech_star, check_in=date_time, )

    if device_id == tech_star.device_id:
        attendance.status = "Uncompleted"
    else:
        attendance.status = "Fraudulent"

    attendance.save()
    serializer = AttendanceSerializer(attendance)
    return serializer.data


class TechStarListCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = TechStarSerializer
    parser_classes = [FormParser, MultiPartParser]
    queryset = TechStar.active_objects.all()


class TechStarDetailsUpdateDeleteAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TechStarDetailSerializer
    parser_classes = [FormParser, MultiPartParser]
    queryset = TechStar.active_objects.all()


class TrashedTechStarListAPIView(AdminOrMembershipManagerOrReadOnlyMixin, ListAPIView):
    queryset = TechStar.inactive_objects.all()
    serializer_class = TechStarSerializer


class TrashedTechStarRestoreAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomDestroyAPIView):
    queryset = TechStar.inactive_objects.all()
    serializer_class = TechStarDetailSerializer


class TestimonialListCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = TestimonialFrontpageSerializer
    queryset = Testimonial.active_objects.all()


class TestimonialFrontpageListAPIView(AdminOrMembershipManagerOrReadOnlyMixin, ListAPIView):
    serializer_class = TestimonialFrontpageSerializer

    def get(self, request, *args, **kwargs):
        testimonial = list(Testimonial.active_objects.all())
        random.shuffle(testimonial)
        serializer = self.get_serializer(testimonial[:5], many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TestimonialDetailUpdateDeleteView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TestimonialDetailSerializer
    queryset = Testimonial.active_objects.all()


class TrashedTestimonialListAPIView(AdminOrMembershipManagerOrReadOnlyMixin, ListAPIView):
    queryset = Testimonial.inactive_objects.all()
    serializer_class = TestimonialSerializer


class TrashedTestimonialRestoreAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomDestroyAPIView):
    queryset = Testimonial.inactive_objects.all()
    serializer_class = TestimonialDetailSerializer


class ResumptionAndClosingTimeCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = ResumptionAndClosingTimeSerializer
    queryset = ResumptionAndClosingTime.objects.all()


class ResumptionAndClosingTimeDetailsUpdateDetailAPIView(AdminOrMembershipManagerOrReadOnlyMixin,
                                                         CustomRetrieveUpdateAPIView):
    serializer_class = ResumptionAndClosingTimeSerializer
    queryset = ResumptionAndClosingTime.objects.all()

    def get_object(self):
        return ResumptionAndClosingTime.objects.all().first()


class GenerateAttendanceQRCode(IsValidRequestAPIKey, CustomCreateAPIView):
    serializer_class = BarcodeSerializer

    def post(self, request, *args, **kwargs):
        if timezone.now().isoweekday() not in valid_days:
            raise ValidationError("Today is not workday !")
        # new_request = decrypt_request(request.data)
        new_request = request.data
        latitude = float(new_request.get("latitude"))
        longitude = float(new_request.get("longitude"))

        if office_location.latitude_1 < latitude < office_location.latitude_2 and \
                office_location.longitude_1 <= longitude <= office_location.longitude_2:
            if time_check.open_time <= timezone.localtime(timezone.now()).time() <= time_check.close_time:

                email = new_request.get("email")
                try:
                    tech_star = TechStar.active_objects.get(official_email=email)
                except:
                    raise ValidationError("Tech Star with this email doesn't exist !")

                date_time = new_request.get("date_time")

                data = {
                    "email": email,
                    "date_time": date_time,
                    "secret_key": config("QR_SECRET_KEY")
                }

                qr = generate_qr(data)
                result = self.get_serializer(qr)

                return Response(result.data, status=HTTP_201_CREATED)
            raise ValidationError("Out of Time Range !")
        raise ValidationError("Out of Location Range")


class RecordAttendanceAPIView(IsValidRequestAPIKey, CustomCreateAPIView):
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        if timezone.now().isoweekday() not in valid_days:
            raise ValidationError("Today is not workday !")
        new_request = request.data
        latitude = float(new_request.get("latitude"))
        longitude = float(new_request.get("longitude"))

        if office_location.latitude_1 < latitude < office_location.latitude_2 and \
                office_location.longitude_1 <= longitude <= office_location.longitude_2:
            if time_check.open_time <= timezone.localtime(timezone.now()).time() <= time_check.close_time:

                email = new_request.get("email")
                date_time = new_request.get("date_time")
                device_id = new_request.get("device_id")

                try:
                    tech_star = TechStar.active_objects.get(official_email=email)
                except:
                    raise ValidationError("Tech Star Does Not Exist !")

                if tech_star.device_id is None:
                    tech_star.device_id = device_id
                    tech_star.save()

                tech_star_attendance = Attendance.active_objects.filter(
                    tech_star_id=tech_star.id).last()

                if tech_star_attendance is not None:
                    last_attendance_date = tech_star_attendance.check_in
                    if last_attendance_date.date() == timezone.now().date():
                        if timezone.now().time() < (last_attendance_date + timezone.timedelta(minutes=30)).time():
                            raise ValidationError("You cannot check out 10 minutes after check in!")

                        tech_star_attendance.check_out = date_time
                        if tech_star_attendance.status == "Uncompleted" and tech_star.device_id == device_id:
                            tech_star_attendance.status = "Successful"
                        elif tech_star.device_id != device_id:
                            tech_star_attendance.status = "Fraudulent"
                        tech_star_attendance.save()
                        attendance = self.get_serializer(tech_star_attendance)
                        return Response(attendance.data, status=HTTP_201_CREATED)
                    attendance = create_attendance(tech_star, date_time, device_id)
                    return Response(attendance, status=HTTP_201_CREATED)
                attendance = create_attendance(tech_star, date_time, device_id)
                return Response(attendance, status=HTTP_201_CREATED)
            raise ValidationError("Out Of Time Range !")
        raise ValidationError("Out of Location Range")


class AttendanceUpdateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    queryset = Attendance.active_objects.all()
    serializer_class = AttendanceSerializer


class AttendanceListAPIView(IsValidRequestAPIKey, ListAPIView):
    queryset = Attendance.active_objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)


class OfficeLocationCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = OfficeLocationSerializer
    queryset = OfficeLocation.objects.all()


class OfficeLocationDetailsUpdateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    serializer_class = OfficeLocationSerializer

    def get_object(self):
        return OfficeLocation.objects.all().first()


class XpertOfTheWeekListCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = XpertOfTheWeekSerializer
    queryset = XpertOfTheWeek.active_objects.all()


class XpertOfTheWeekDetailUpdateDeleteAPIView(AdminOrMembershipManagerOrReadOnlyMixin,
                                              CustomRetrieveUpdateDestroyAPIView):
    serializer_class = XpertOfTheWeekDetailSerializer
    queryset = XpertOfTheWeek.active_objects.all()


class TrashedXpertListAPIView(AdminOrMembershipManagerOrReadOnlyMixin, ListAPIView):
    queryset = XpertOfTheWeek.inactive_objects.all()
    serializer_class = XpertOfTheWeekSerializer


class TrashedXpertRestoreAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomDestroyAPIView):
    queryset = XpertOfTheWeek.inactive_objects.all()
    serializer_class = XpertOfTheWeekSerializer


class WriteAdminLog(IsValidRequestAPIKey, APIView):

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        event = new_request.get('event')
        admin = new_request.get("admin")
        message = new_request.get("message")

        if event is None or admin is None or message is None:
            raise ValidationError("Incomplete Data")

        write_log_csv(event, admin, message)

        return Response("Activity logged successfully", status=HTTP_201_CREATED)


class ReadAdminLog(IsValidRequestAPIKey, ListAPIView):
    def get(self, *args, **kwargs):
        with open("admin_activity_logs.csv", "r") as x:
            read = literal_eval(json.dumps(list(csv.DictReader(x))))
            return Response(read, status=HTTP_200_OK)
