from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from .models import FrequentlyAskedQuestions, ContactUs


class FrequentlyAskedQuestionsSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="support:faq_details_update_delete", read_only=True)

    class Meta:
        model = FrequentlyAskedQuestions
        fields = (
            "id",
            "question",
            "answer",
            "url"
        )


class FrequentlyAskedQuestionsDetailSerializer(ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestions
        fields = (
            "id",
            "question",
            "answer",
        )


class ContactUsSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="support:contact_us_details_update_delete", read_only=True)

    class Meta:
        model = ContactUs
        fields = (
            "id",
            "full_name",
            "email",
            "subject",
            "short_message",
            "url",
            "message",
        )

        extra_kwargs = {
            "message": {"write_only": True},
            "short_message": {"read_only": True}
        }


class ContactUsDetailSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            "id",
            "full_name",
            "subject",
            "email",
            "message",
        )