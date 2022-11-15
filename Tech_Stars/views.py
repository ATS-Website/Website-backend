import csv
import datetime
import json
import random

from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    TestimonialSerializer, TestimonialDetailSerializer,
    TechStarSerializer, TechStarDetailSerializer,
    BarcodeSerializer, ResumptionAndClosingTimeSerializer, AttendanceSerializer,
    OfficeLocationSerializer, TestimonialFrontpageSerializer, XpertOfTheWeekSerializer,
    XpertOfTheWeekDetailSerializer
)
from .renderers import CustomRenderer
from .models import Testimonial, TechStar, ResumptionAndClosingTime, Attendance, OfficeLocation, XpertOfTheWeek
from .mixins import (AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView,
                     CustomRetrieveUpdateDestroyAPIView, CustomCreateAPIView,
                     CustomRetrieveUpdateAPIView
                     )
from .utils import generate_qr, write_log_csv
from .enc_dec.encryption_decryption import aes_encrypt
from Accounts.mixins import IsAdminOrReadOnlyMixin


# Create your views here.


timezone.activate(settings.TIME_ZONE)


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
    renderer_classes = (CustomRenderer,)


class TechStarDetailsUpdateDeleteAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TechStarDetailSerializer
    parser_classes = [FormParser, MultiPartParser]
    queryset = TechStar.active_objects.all()
    renderer_classes = (CustomRenderer,)


class TestimonialListCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.active_objects.all()
    renderer_classes = (CustomRenderer,)


class TestimonialFrontpageListAPIView(AdminOrMembershipManagerOrReadOnlyMixin, ListAPIView):
    serializer_class = TestimonialFrontpageSerializer
    renderer_classes = (CustomRenderer,)

    def get(self, request, *args, **kwargs):
        testimonial = list(Testimonial.active_objects.all())
        random.shuffle(testimonial)
        serializer = self.get_serializer(testimonial[:6], many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TestimonialDetailUpdateDeleteView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TestimonialDetailSerializer
    queryset = Testimonial.active_objects.all()
    renderer_classes = (CustomRenderer,)


class ResumptionAndClosingTimeCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = ResumptionAndClosingTimeSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomRenderer,)
    queryset = ResumptionAndClosingTime.objects.all()


class ResumptionAndClosingTimeDetailsUpdateDetailAPIView(AdminOrMembershipManagerOrReadOnlyMixin,
                                                         CustomRetrieveUpdateAPIView):
    serializer_class = ResumptionAndClosingTimeSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomRenderer,)
    queryset = ResumptionAndClosingTime.objects.all()

    def get_object(self):
        return ResumptionAndClosingTime.objects.all().first()


class GenerateAttendanceQRCode(CustomCreateAPIView):
    renderer_classes = (CustomRenderer,)

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
        }
        print(data)

        qr = generate_qr(aes_encrypt(data))
        result = BarcodeSerializer(qr)

        return Response(result.data, status=HTTP_201_CREATED)
        raise ValidationError("Out of Time Range !")


class RecordAttendanceAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomCreateAPIView):
    renderer_classes = (CustomRenderer,)
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        latitude = float(new_request.get("latitude"))
        longitude = float(new_request.get("longitude"))
        office_location = OfficeLocation.objects.all().first()

        if office_location.latitude_1 < latitude < office_location.latitude_2 \
                and office_location.longitude_1 <= longitude <= office_location.longitude_2:

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
                    last_attendance_date = str(
                        tech_star_attendance.check_in)[:10]
                    if last_attendance_date == str(timezone.localtime(timezone.now()).date()):
                        # print(date_time)
                        # print(tech_star_attendance.check_in)
                        # print((tech_star_attendance.check_in + datetime.timedelta(minutes=10)))
                        # if date_time > tech_star_attendance.check_in + datetime.timedelta(minutes=10):
                        #     raise ValidationError(
                        #         "You cannot check out, if the time is not 2 hours from your check in !")

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
    renderer_classes = (CustomRenderer,)


class AttendanceListAPIView(ListAPIView):
    queryset = Attendance.active_objects.all()
    serializer_class = AttendanceSerializer
    renderer_classes = (CustomRenderer,)
    permission_classes = (IsAuthenticated,)


class OfficeLocationCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = OfficeLocationSerializer
    renderer_classes = (CustomRenderer,)
    queryset = OfficeLocation.objects.all()


class OfficeLocationDetailsUpdateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    serializer_class = OfficeLocationSerializer
    renderer_classes = (CustomRenderer,)

    def get_object(self):
        return OfficeLocation.objects.all().first()


class XpertOfTheWeekListCreateAPIView(AdminOrMembershipManagerOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = XpertOfTheWeekSerializer
    renderer_classes = (CustomRenderer,)
    queryset = XpertOfTheWeek.active_objects.all()


class XpertOfTheWeekDetailUpdateDeleteAPIView(AdminOrMembershipManagerOrReadOnlyMixin,
                                              CustomRetrieveUpdateDestroyAPIView):
    serializer_class = XpertOfTheWeekDetailSerializer
    renderer_classes = (CustomRenderer,)
    queryset = XpertOfTheWeek.active_objects.all()


class WriteAdminLog(APIView):
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


class ReadAdminLog(IsAdminOrReadOnlyMixin, ListAPIView):
    def get(self, *args, **kwargs):
        with open("admin_activity_logs.csv", "r") as x:
            read = json.dumps(list(csv.DictReader(x)))
            return Response(read, status=HTTP_200_OK)
