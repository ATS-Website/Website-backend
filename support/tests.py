from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from decouple import config

from accounts.models import Account

from support.models import FrequentlyAskedQuestions, ContactUs


# Create your tests here.


# client = APIClient()


class FAQTests(APITestCase):

    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com")
        return user

    @classmethod
    def setUpTestData(cls):
        questions = ["where are you ?", "where do you live ?", "what do you do ?"]
        answers = ["I am at home.", "West Africa/Africa.", "Eat Junks"]

        for number in range(0, 2):
            FrequentlyAskedQuestions.active_objects.create(question=questions[number], answer=answers[number])

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
        self.assertGreater(len(response.data), 0)

    def test_create_update_FAQ(self):
        self.client.credentials(**self.request_headers)
        url = reverse("support:faq_list_create")
        data = {
            "question": "who are you ?",
            "answer": "i am me !"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_get_single_FAQ(self):
        self.client.credentials(**self.request_headers)
        get_url = reverse("support:faq_details_update_delete", kwargs={"pk": 1})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_update_FAQ(self):
        self.client.credentials(**self.request_headers)
        update_url = reverse("support:faq_details_update_delete", kwargs={"pk": 1})
        update_data = {
            "question": "who are you ?",
            "answer": "i am Not You !"
        }
        response = self.client.put(update_url, data=update_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_delete_FAQ(self):
        self.client.credentials(**self.request_headers)
        delete_url = reverse("support:faq_details_update_delete", kwargs={"pk": 1})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(FrequentlyAskedQuestions.active_objects.filter(id=1).first(), None)


class ContactUsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        full_name = ["samuel", "azubuine", "tochukwu", "cornelius"]
        subject = ["this", "is", "to", "test"]
        message = ["This", "is", "to", "test"]
        email = ["samuel@gmail.com", "azuibuine@gmail.com", "tochukwu@gmail.com", "cornelius@gmail.com"]

        for number in range(0, 4):
            ContactUs.active_objects.create(
                full_name=full_name[number],
                message=message[number],
                subject=subject[number],
                email=email[number]
            )

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
        self.assertGreater(len(response.data), 0)

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

    def test_get_contact_us(self):
        self.client.credentials(**self.request_headers)
        get_url = reverse("support:contact_us_details_update_delete", args=[1])
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_update_contact_us(self):
        self.client.credentials(**self.request_headers)
        update_url = reverse("support:contact_us_details_update_delete", args=[1])
        data = {
            "full_name": "Hello Worldie!",
            "subject": "new Test",
            "message": "Just Testing update",
            "email": "test@test.com"
        }

        response = self.client.put(update_url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_delete_contact_us(self):
        self.client.credentials(**self.request_headers)
        delete_url = reverse("support:contact_us_details_update_delete", args=[1])
        response = self.client.delete(delete_url)
        print(response.content)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
