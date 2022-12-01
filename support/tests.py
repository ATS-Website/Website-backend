from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

# Create your tests here.


client = APIClient()


class FAQTests(APITestCase):

    def test_list_faq(self):
        url = reverse("support:faq_list_create")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_FAQ(self):
        url = reverse("support:faq_list_create")
        data = {
            "question": "who are you ?",
            "answer": "i am me !"
        }
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)


class ContactUsTests(APITestCase):
    def test_list_contact_us(self):
        url = reverse("support:contact_us_list_create")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_contact_us(self):
        url = reverse("support:contact_us_list_create")
        data = {
            "full_name": "Hello World !",
            "subject": "Test",
            "message": "Just Testing",
            "email": "test@test.com"
        }

        response = client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
