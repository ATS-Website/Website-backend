from rest_framework.serializers import (ModelSerializer, HyperlinkedIdentityField,
                                        Serializer, CharField
                                        )

from .models import TechStar, Testimonial, ResumptionAndClosingTime, Attendance, OfficeLocation, XpertOfTheWeek


class TechStarSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="Tech_Stars:tech_star_details_update_delete", read_only=True)

    class Meta:
        model = TechStar
        fields = (
            "id",
            "tech_star_id",
            "full_name",
            "course",
            "profile_picture",
            "self_description",
            "favorite_meal",
            "favorite_quote",
            "cohort",
            "official_email",
            "url"

        )
        extra_kwargs = {
            "tech_star_id": {"read_only": True},
            "self_description": {"write_only": True},
            "favorite_meal": {"write_only": True},
            "favorite_quote": {"write_only": True},
        }

    def create(self, validated_data):
        tech_star = TechStar.objects.filter().last()

        if tech_star is not None:
            get_id = int(str(tech_star.tech_star_id).split("-")[-1]) + 1

            id2string = f"ATS-{str(get_id).zfill(4)}"

            validated_data['tech_star_id'] = id2string

        else:
            validated_data['tech_star_id'] = f"ATS-0001"

        return TechStar.active_objects.create(**validated_data)


class TechStarDetailSerializer(ModelSerializer):
    class Meta:
        model = TechStar
        fields = (
            "id",
            "tech_star_id",
            "full_name",
            "course",
            "profile_picture",
            "cohort",
            "self_description",
            "favorite_meal",
            "favorite_quote",
            "device_id",
            "official_email",
        )
        extra_kwargs = {
            "tech_star_id": {"read_only": True}
        }


class TestimonialSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(
        view_name="Tech_Stars:testimonial_detail_update_delete", read_only=True)

    class Meta:
        model = Testimonial
        fields = (
            "id",
            "tech_star",
            "testimonial",
            "url"
        )


class TestimonialDetailSerializer(ModelSerializer):
    class Meta:
        model = Testimonial
        fields = (
            "id",
            "tech_star",
            "testimonial"
        )


class TestimonialFrontpageSerializer(ModelSerializer):
    class Meta:
        model = Testimonial
        fields = (
            "id",
            "tech_star_full_name",
            "testimonial",
            # "tech_star_profile_picture",
            "tech_star_cohort",
            "tech_star_course"

        )


class BarcodeSerializer(Serializer):
    file_type = CharField(max_length=10)
    image_base64 = CharField(max_length=500)


class ResumptionAndClosingTimeSerializer(ModelSerializer):
    class Meta:
        model = ResumptionAndClosingTime
        fields = (
            "open_time",
            "close_time"
        )


class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            "id",
            "status",
            "tech_star",
            "check_in",
            "check_out",
        )


class OfficeLocationSerializer(ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = (
            "latitude_1",
            "latitude_2",
            "longitude_1",
            "longitude_2",
        )


class XpertOfTheWeekSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(
        view_name="Tech_Stars:xpert_detail_update_delete", read_only=True)

    class Meta:
        model = XpertOfTheWeek
        fields = (
            "tech_star",
            "interview",
            "url"
        )
        extra_kwargs = {
            "interview": {"write_only": True}
        }


class XpertOfTheWeekDetailSerializer(ModelSerializer):
    class Meta:
        model = XpertOfTheWeek
        fields = (
            "tech_star",
            "interview"
        )
