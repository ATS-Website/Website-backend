import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from decouple import config

from accounts.models import Account
from blogs.models import Category, NewsLetter


# Create your tests here

class CategoryTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
        return user

    @classmethod
    def setUpTestData(cls):
        name = ["Administration", "Events", "Lifestyle"]

        for number in range(0, 2):
            Category.active_objects.create(name=name[number])

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

    def test_category_list(self):
        self.client.credentials(**self.request_headers)
        url = reverse("blogs:category_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_category(self):
        self.client.credentials(**self.request_headers)
        url = reverse("blogs:category_list_create")
        data = {
            "name": "Agriculture",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_get_single_category(self):
        self.client.credentials(**self.request_headers)
        get_url = reverse("blogs:category_detail_update_delete", kwargs={"pk": 1})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_update_category(self):
        self.client.credentials(**self.request_headers)
        update_url = reverse("blogs:category_detail_update_delete", kwargs={"pk": 1})
        update_data = {
            "name": "Entertainment"
        }
        response = self.client.put(update_url, data=update_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_delete_category(self):
        self.client.credentials(**self.request_headers)
        delete_url = reverse("blogs:category_detail_update_delete", kwargs={"pk": 1})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Category.active_objects.filter(id=1).first(), None)


class NewsletterTest(APITestCase):
    @classmethod
    def setUp(cls):
        user, x = Account.active_objects.get_or_create(username="TestMan", first_name="The", last_name="tester",
                                                       password="Password@1",
                                                       email="test@afexnigeria.com", is_superadmin=True)
        return user

    @classmethod
    def setUpTestData(cls):
        title = ["This", "Is", "A", "Test"]
        subject = title.copy()
        content = title.copy()

        for number in range(0, 2):
            NewsLetter.active_objects.create(title=title[number], subject=subject[number], content=content[number])

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

    def test_category_list(self):
        self.client.credentials(**self.request_headers)
        url = reverse("blogs:newsletter_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_category(self):
        self.client.credentials(**self.request_headers)
        url = reverse("blogs:newsletter_list_create")
        data = {
            "title": "ATS",
            "subject": "ATS First News Letter",
            "message": "Let's Go !"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_get_single_category(self):
        self.client.credentials(**self.request_headers)
        get_url = reverse("blogs:newsletter_details_update_delete", kwargs={"pk": 1})
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_update_category(self):
        self.client.credentials(**self.request_headers)
        update_url = reverse("blogs:newsletter_details_update_delete", kwargs={"pk": 1})
        update_data = {
            "title": "ATS",
            "subject": "ATS First News Letter",
            "message": "Changed"
        }
        response = self.client.put(update_url, data=update_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_delete_category(self):
        self.client.credentials(**self.request_headers)
        delete_url = reverse("blogs:newsletter_details_update_delete", kwargs={"pk": 1})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Category.active_objects.filter(id=1).first(), None)



class AuthorsTest(APITestCase):

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

    def test_list_of_authors(self):
        self.client.credentials(**self.request_headers)
        url = reverse("blogs:blog_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)


class BlogsTest(APITestCase):
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
        url = reverse("blogs:blog_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)


class NewsTest(APITestCase):
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
        url = reverse("blogs:news_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)




