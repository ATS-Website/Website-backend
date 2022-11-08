import datetime
import random

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
import qrcode

from .permissions import IsAdminOrReadOnly
from .serializers import (
                          TestimonialSerializer, TestimonialDetailSerializer,
                          TechStarSerializer, TechStarDetailSerializer,
                          BarcodeSerializer, ResumptionAndClosingTimeSerializer, AttendanceSerializer,
                          OfficeLocationSerializer, TestimonialFrontpageSerializer
                          )
from .renderers import CustomRenderer
from .models import Testimonial, TechStar, ResumptionAndClosingTime, Attendance, OfficeLocation
from .mixins import (AdminOrReadOnlyMixin, CustomListCreateAPIView,
                     CustomRetrieveUpdateDestroyAPIView, CustomCreateAPIView,
                     CustomRetrieveUpdateAPIView
                     )
from .utils import generate_qr


# Create your views here.
def create_attendance(tech_star, date_time, device_id):
    attendance = Attendance.active_objects.create(tech_star=tech_star, check_in=date_time, )

    if device_id == tech_star.device_id:
        attendance.status = "Uncompleted"
    else:
        attendance.status = "Fraudulent"

    attendance.save()
    serializer = AttendanceSerializer(attendance)
    return serializer.data


class TechStarListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = TechStarSerializer
    queryset = TechStar.active_objects.all()
    renderer_classes = (CustomRenderer,)
    model = "TechStar"


class TechStarDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TechStarDetailSerializer
    queryset = TechStar.active_objects.all()
    renderer_classes = (CustomRenderer,)

    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.is_active = True
    #     instance.save()
    #     return super().delete(request, *args, **kwargs)


class TestimonialListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.active_objects.all()
    renderer_classes = (CustomRenderer,)


class TestimonialFrontpageListAPIView(ListAPIView):
    serializer_class = TestimonialFrontpageSerializer
    renderer_classes = (CustomRenderer,)

    def get(self, request, *args, **kwargs):
        testimonial = list(Testimonial.active_objects.all())
        random.shuffle(testimonial)
        print(testimonial)
        serializer = self.get_serializer(testimonial[:6], many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TestimonialDetailUpdateDeleteView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    serializer_class = TestimonialDetailSerializer
    queryset = Testimonial.active_objects.all()
    renderer_classes = (CustomRenderer,)

    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.is_active = True
    #     instance.save()
    #     return super().delete(request, *args, **kwargs)


class ResumptionAndClosingTimeCreateAPIView(CustomListCreateAPIView):
    serializer_class = ResumptionAndClosingTimeSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomRenderer,)
    queryset = ResumptionAndClosingTime.objects.all()


class ResumptionAndClosingTimeDetailsUpdateDetailAPIView(CustomRetrieveUpdateAPIView):
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
        time_check = ResumptionAndClosingTime.objects.all().first()

        open_time = time_check.open_time
        close_time = time_check.close_time

        # if open_time <= datetime.datetime.now().time() <= close_time:

        email = request.data.get("email")
        try:
            tech_star = TechStar.active_objects.get(official_email=email)
        except:
            raise ValidationError("Tech Star Not Found !")

        date_time = request.data.get("date_time")
        location = request.data.get("location")

        data = {
            "email": email,
            "date_time": date_time,
        }
        print(data)

        qr = generate_qr(data)
        result = BarcodeSerializer(qr)

        return Response(result.data, status=HTTP_201_CREATED)
        raise ValidationError("Out of Time Range !")


class RecordAttendanceAPIView(CustomCreateAPIView):
    renderer_classes = (CustomRenderer,)
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        latitude = float(request.data.get("latitude"))
        longitude = float(request.data.get("longitude"))
        office_location = OfficeLocation.objects.all().first()

        if office_location.latitude_1 < latitude < office_location.latitude_2 \
                and office_location.longitude_1 <= longitude <= office_location.longitude_2:

            email = request.data.get("email")
            date_time = request.data.get("date_time")
            device_id = request.data.get("device_id")

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

            if open_time <= datetime.datetime.now().time() <= close_time:
                tech_star_attendance = Attendance.active_objects.filter(tech_star_id=tech_star.id).first()
                if tech_star_attendance is not None:
                    last_attendance_date = str(tech_star_attendance.check_in)[:10]
                    if last_attendance_date == str(datetime.datetime.now().date()):
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
                    attendance = create_attendance(tech_star, date_time, device_id)
                    return Response(attendance, status=HTTP_201_CREATED)
                attendance = create_attendance(tech_star, date_time, device_id)
                return Response(attendance, status=HTTP_201_CREATED)
            raise ValidationError("Out Of Time Range !")
        raise ValidationError("Out of Location Range")


class AttendanceUpdateAPIView(CustomRetrieveUpdateAPIView):
    queryset = Attendance.active_objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomRenderer,)


class AttendanceListAPIView(ListAPIView):
    queryset = Attendance.active_objects.all()
    serializer_class = AttendanceSerializer
    renderer_classes = (CustomRenderer,)
    permission_classes = (IsAuthenticated,)


class OfficeLocationCreateAPIView(CustomListCreateAPIView):
    serializer_class = OfficeLocationSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomRenderer,)
    queryset = OfficeLocation.objects.all()


class OfficeLocationDetailsUpdateAPIView(CustomRetrieveUpdateAPIView):
    serializer_class = OfficeLocationSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomRenderer,)

    def get_object(self):
        return OfficeLocation.objects.all().first()
