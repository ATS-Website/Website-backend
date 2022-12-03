import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK
from decouple import config

from accounts.models import Account


# Create your tests here


class TechStarTest(APITestCase):
    file_url = r"media/work01-hover.jpg"

    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
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

    def test_list_of_tech_stars(self):
        self.client.credentials(**self.request_headers)
        url = reverse("tech_stars:tech_star_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)


class TestimonialsTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
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

    def test_list_of_testimonial(self):
        self.client.credentials(**self.request_headers)
        url = reverse("tech_stars:testimonial_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)


class AttendanceTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
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

    def test_list_attendance(self):
        self.client.credentials(**self.request_headers)
        url = reverse("tech_stars:attendance_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)


class XpertOfTheWeekTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
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

    def test_Xpert_of_the_week_list(self):
        self.client.credentials(**self.request_headers)
        url = reverse("tech_stars:xpert_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)


class ResumptiontTimeTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
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

    def test_len_resumption_object(self):
        self.client.credentials(**self.request_headers)
        url = reverse("tech_stars:office_location_create")
        response = self.client.get(url)
        result = json.loads(response.content.decode("utf8")).get("data").get("results")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertLess(len(result), 2)


class OfficeLocationTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
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

    def test_len_resumption_object(self):
        self.client.credentials(**self.request_headers)
        url = reverse("tech_stars:resumption_closing_time_create")
        response = self.client.get(url)
        result = json.loads(response.content.decode("utf8")).get("data").get("results")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertLess(len(result), 2)
