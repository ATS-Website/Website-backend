from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from .models import FrequentlyAskedQuestions, ContactUs


class FrequentlyAskedQuestionsSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Support:faq_details_update_delete", read_only=True)

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
    url = HyperlinkedIdentityField(view_name="Support:contact_us_details_update_delete", read_only=True)

    class Meta:
        model = ContactUs
        fields = (
            "id",
            "full_name",
            "email",
            # "short_message",
            "url",
        )


class ContactUsDetailSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            "id",
            "full_name",
            "email",
            "message",
        )
