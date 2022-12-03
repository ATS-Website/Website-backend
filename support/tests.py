from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from decouple import config

from accounts.models import Account

from support.models import FrequentlyAskedQuestions


# Create your tests here.


# client = APIClient()


class FAQTests(APITestCase):

    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com")

        return user

    @property
    def get_token(self):
        return RefreshToken.for_user(self.setUp()).access_token

    @property
    def request_headers(self):
        headers = {
            "HTTP_API_KEY": config("APP_API_KEY"),
            "HTTP_HASH_KEY": config("HASH_KEY"),
            "HTTP_REQUEST_TS": config("REQUEST_TS"),
            'HTTP_AUTHORIZATION': f"Bearer {self.get_token}"

        }
        return headers

    def test_list_faq(self):
        self.client.credentials(**self.request_headers)
        url = reverse("support:faq_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_update_FAQ(self):
        self.client.credentials(**self.request_headers)
        url = reverse("support:faq_list_create")
        data = {
            "question": "who are you ?",
            "answer": "i am me !"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        update_url = reverse("support:faq_details_update_delete", kwargs={"pk": 1})
        update_data = {
            "question": "who are you ?",
            "answer": "i am Not You !"
        }
        response = self.client.put(update_url, data=update_data)
        print(vars(response))
        self.assertEqual(response.status_code, HTTP_201_CREATED)


class ContactUsTests(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com")

        return user

    @property
    def get_token(self):
        return RefreshToken.for_user(self.setUp()).access_token

    @property
    def request_headers(self):
        headers = {
            "HTTP_API_KEY": config("APP_API_KEY"),
            "HTTP_HASH_KEY": config("HASH_KEY"),
            "HTTP_REQUEST_TS": config("REQUEST_TS"),
            'HTTP_AUTHORIZATION': f"Bearer {self.get_token}"
        }
        return headers

    def test_list_contact_us(self):
        self.client.credentials(**self.request_headers)
        url = reverse("support:contact_us_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_contact_us(self):
        self.client.credentials(**self.request_headers)
        url = reverse("support:contact_us_list_create")
        data = {
            "full_name": "Hello World !",
            "subject": "Test",
            "message": "Just Testing",
            "email": "test@test.com"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
