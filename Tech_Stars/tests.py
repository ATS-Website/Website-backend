from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase, APIClient

from Accounts.models import Account

# Create your tests here.
client = APIClient()


class TechStarTest(APITestCase):

    def test_list_of_tech_stars(self):
        url = reverse("Tech_Stars:tech_star_list_create")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_create_tech_stars(self):
        data = {
                "full_name": "john_chukwudi",
                "program": "1",
                "self_description": "cool and calm",
                "official_email": "johnchukwdi@gmail.com",
                "favorite_meal": "snacks",
                "favorite_quote": "No Matter What , always eat",
                "year": "2022"
        }
        url = reverse("Tech_Stars:tech_star_list_create")
        response = client.post(url, data,  format="json")
        print(response)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
