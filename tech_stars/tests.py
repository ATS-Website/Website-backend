from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APITestCase, APIClient, RequestsClient, CoreAPIClient
from requests.auth import HTTPBasicAuth
from decouple import config

from accounts.models import Account

# Create your tests here

# with open("media/work01-hover.jpg", "rb") as x:
#     profile_picture = x.read()

headers = {
    "api-key": config("APP_API_KEY"),
    "hash-key": config("HASH_KEY"),
    "request-ts": config("REQUEST_TS")
}

# client = CoreAPIClient()
# client.auth = HTTPBasicAuth("user", "pass")
# client.headers.update(headers)


client = RequestsClient()
client.auth = HTTPBasicAuth('user', 'pass')
client.headers.update({'x-test': 'true'})


class TechStarTest(APITestCase):

    def test_list_of_tech_stars(self):
        url = reverse("tech_stars:tech_star_list_create")
        # response = client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    # def test_create_tech_stars(self):
    #     data = {
    #             "full_name": "john_chukwudi",
    #             "program": "1",
    #             "self_description": "cool and calm",
    #             "official_email": "johnchukwdi@gmail.com",
    #             "favorite_meal": "snacks",
    #             "favorite_quote": "No Matter What , always eat",
    #             "year": "2022"
    #     }
    #     url = reverse("tech_stars:tech_star_list_create")
    #     response = client.post(url, data,  format="json")
    #     print(response)
    #     self.assertEqual(response.status_code, HTTP_201_CREATED)

# class TestimonialsTest(APITestCase):
#     def test_list_of_testimonial(self):
#         url = reverse("tech_stars:testimonial_list_create")
#         response = client.get(url)
#         self.assertEqual(response.status_code, HTTP_200_OK)
