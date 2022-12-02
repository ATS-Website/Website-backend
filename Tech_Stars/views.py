from rest_framework.generics import GenericAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
import csv
import datetime
import json
import random
from ast import literal_eval

from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from decouple import config
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import CompoundSearchFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from Blogs.permissions import IsAdminOrReadOnly
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
from .utils import generate_qr_code, generate_qr
from .tasks import write_log_csv
from .enc_dec.encryption_decryption import aes_encrypt
from Accounts.mixins import IsAdminOrReadOnlyMixin


# Create your views here.


# timezone.activate(settings.TIME_ZONE)

class TechStarDocumentView(DocumentViewSet):
    document = TechStarDocument
    serializer_class = TechStarDocumentSerializer

    filter_backends = [CompoundSearchFilterBackend, SuggesterFilterBackend]
    search_fields = {
        "full_name": {'fuzziness': 'AUTO'},
        "official_email": {'fuzziness': 'AUTO'},
        "self_description": {'fuzziness': 'AUTO'},
        "course": {'fuzziness': 'AUTO'},

    }
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
    multi_match_search_fields = ("full_name", "official_email", "self_description")
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


class TechStarListCreateAPIView(CustomListCreateAPIView):
    serializer_class = TechStarSerializer
    parser_classes = [FormParser, MultiPartParser]
    queryset = TechStar.active_objects.all()


class TechStarDetailsUpdateDeleteAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TechStarDetailSerializer
    parser_classes = [FormParser, MultiPartParser]
    queryset = TechStar.active_objects.all()


class TrashedTechStarListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = TechStar.inactive_objects.all()
    serializer_class = TechStarSerializer


class TrashedTechStarRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = TechStar.inactive_objects.all()
    serializer_class = TechStarDetailSerializer


class TestimonialListCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.active_objects.all()


class TestimonialFrontpageListAPIView(AdminOrMembershipManagerOrReadOnlyMixin, ListAPIView):
    serializer_class = TestimonialFrontpageSerializer

    def get(self, request, *args, **kwargs):
        testimonial = list(Testimonial.active_objects.all())
        random.shuffle(testimonial)
        serializer = self.get_serializer(testimonial[:6], many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TestimonialDetailUpdateDeleteView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TestimonialDetailSerializer
    queryset = Testimonial.active_objects.all()


class TrashedTestimonialListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = Testimonial.inactive_objects.all()
    serializer_class = TestimonialSerializer


class TrashedTestimonialRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
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


class GenerateAttendanceQRCode(CustomCreateAPIView):
    serializer_class = BarcodeSerializer

    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        time_check = ResumptionAndClosingTime.objects.all().first()

        # open_time = time_check.open_time
        # close_time = time_check.close_time

        # if open_time <= timezone.localtime(timezone.now()).time() <= close_time:

        email = new_request.get("email")
        try:
            tech_star = TechStar.active_objects.get(official_email=email)
        except:
            raise ValidationError("Tech Star with this email doesn't exist !")

        date_time = new_request.get("date_time")
        location = new_request.get("location")

        data = {
            "email": email,
            "date_time": date_time,
            "secret_key": config("QR_SECRET_KEY")
        }

        qr = generate_qr(aes_encrypt(data))
        result = self.get_serializer(qr)

        return Response(result.data, status=HTTP_201_CREATED)
        raise ValidationError("Out of Time Range !")


class RecordAttendanceAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomCreateAPIView):
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        latitude = float(new_request.get("latitude"))
        longitude = float(new_request.get("longitude"))
        office_location = OfficeLocation.objects.all().first()

        if office_location.latitude_1 < latitude < office_location.latitude_2 and office_location.longitude_1 <= longitude <= office_location.longitude_2:

            email = new_request.get("email")
            date_time = new_request.get("date_time")
            device_id = new_request.get("device_id")

            try:
                tech_star = TechStar.active_objects.get(official_email=email)
            except:
                raise ValidationError("Tech Star Does Not Exist !")

            time_check = ResumptionAndClosingTime.objects.all().first()

            open_time = time_check.open_time
            close_time = time_check.close_time

            if tech_star.device_id is None:
                tech_star.device_id = device_id
                tech_star.save()

            if open_time <= timezone.localtime(timezone.now()).time() <= close_time:
                tech_star_attendance = Attendance.active_objects.filter(
                    tech_star_id=tech_star.id).first()
                if tech_star_attendance is not None:
                    last_attendance_date = tech_star_attendance.check_in.date()
                    if last_attendance_date == timezone.now().date():
                        date_time_conv = timezone.datetime.strptime(date_time.split(".")[0],
                                                                    "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                        # print(date_time_conv < (tech_star_attendance.check_in + timezone.timedelta(minutes=10)).replace(tzinfo=timezone.utc))
                        # raise ValidationError("")
                        if date_time_conv < (tech_star_attendance.check_in + timezone.timedelta(minutes=10)).replace(
                                tzinfo=timezone.utc):
                            raise ValidationError(
                                "You cannot check out, if the time is not 2 hours from your check in !")

                        tech_star_attendance.check_out = date_time
                        if tech_star_attendance.status == "Uncompleted":
                            tech_star_attendance.status = "Successful"
                        else:
                            pass
                        tech_star_attendance.save()
                        attendance = self.get_serializer(tech_star_attendance)
                        return Response(attendance.data, status=HTTP_201_CREATED)
                    attendance = create_attendance(
                        tech_star, date_time, device_id)
                    return Response(attendance, status=HTTP_201_CREATED)
                attendance = create_attendance(tech_star, date_time, device_id)
                return Response(attendance, status=HTTP_201_CREATED)
            raise ValidationError("Out Of Time Range !")
        raise ValidationError("Out of Location Range")


class AttendanceUpdateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    queryset = Attendance.active_objects.all()
    serializer_class = AttendanceSerializer


class AttendanceListAPIView(ListAPIView):
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


class TrashedXpertListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = XpertOfTheWeek.inactive_objects.all()
    serializer_class = XpertOfTheWeekSerializer


class TrashedXpertRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = XpertOfTheWeek.inactive_objects.all()
    serializer_class = XpertOfTheWeekSerializer


class WriteAdminLog(APIView):

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        event = new_request.get('event')
        admin = new_request.get("admin")
        message = new_request.get("message")

        if event is None or admin is None or message is None:
            raise ValidationError("Incomplete Data")

        write_log_csv.delay(event, admin, message)

        return Response("Activity logged successfully", status=HTTP_201_CREATED)


# class ReadAdminLog(IsAdminOrReadOnlyMixin, GenericAPIView):
class ReadAdminLog(ListAPIView):
    def get(self, *args, **kwargs):
        with open("admin_activity_logs.csv", "r") as x:
            read = literal_eval(json.dumps(list(csv.DictReader(x))))
            return Response(read, status=HTTP_200_OK)
