from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from .models import Program, TechStar, Testimonial


class ProgramSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Tech_Stars:program_detail_update_delete", read_only=True)

    class Meta:
        model = Program
        fields = (
            "id",
            "name",
            "description",
            "url",
        )


class ProgramDetailSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = (
            "id",
            "name",
            "description"
        )


class TechStarSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Tech_Stars:tech_star_details_update_delete", read_only=True)

    class Meta:
        model = TechStar
        fields = (
            "id",
            "tech_star_id",
            "full_name",
            "program",
            "profile_picture",
            "self_description",
            "favorite_meal",
            "favorite_quote",
            "year",
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
        tech_star = TechStar.objects.filter()

        if tech_star[-1] is not None:
            try:
                get_id = int(tech_star[-1].tech_star_id[-4::]) + 1
            except:
                get_id = int(tech_star[-2].tech_star_id[-4::]) + 1

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
            "program",
            "profile_picture",
            "year",
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
    url = HyperlinkedIdentityField(view_name="Tech_Stars:testimonial_detail_update_delete", read_only=True)

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
