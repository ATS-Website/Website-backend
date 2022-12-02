from django.test import TestCase
from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from ..models import BlogArticle
from accounts.models import Account


CREATE_BLOG_URL = reverse('blogs:blog_list_create')


def test_login_required_to_create_blog(self):
    """Test that login is required to access the Endpoint"""
    res = self.client.post(CREATE_BLOG_URL)
    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


def create_blog(**params):
    return BlogArticle.objects.create(**params)


# //private - User modify

class PublicBlogApiTests(TestCase):
    """Test the accounts API(public)"""

    def setUp(self):
        self.client = APIClient()


class PrivateBlogsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create_superuser(username='sammyllee', first_name="sam",
                                                     last_name='azubuine', email='sammy@gmail.com', password='adminadmin')
        self.client.force_authenticate(self.user)

    def test_create_blog_success(self):
        """Test creating blog with valid payload is successful"""

        payload = {
            "title": "50 Investors Share The Best Investment Advice they’ve receive",
            "intro": "January you’ve heard it before “buy low and sell high” “save for the rainy days” and “apply the 50–30–20 rule”, everyone at some point has received a slice of wisdom that helped them make better financial decisions.\n\nWhen it comes to accumulating wealth, it’s important you stay in a constant learning mode grasping all the financial insights you can get. Also, if you take a closer look, most succes",
            "description": "January you’ve heard it before “buy low and sell high” “save for the rainy days” and “apply the 50–30–20 rule”, everyone at some point has received a slice of wisdom that helped them make better financial decisions.\n\nWhen it comes to accumulating wealth, it’s important you stay in a constant learning mode grasping all the financial insights you can get. Also, if you take a closer look, most successful investors have one thing in common — they have rules which are simply a diverse set of information to help them make a fortune. However, until you implement that advice, it’s hard to know what will work for you.\n\nHence, we asked 5investors across various fields what is the absolute best investment advice they have ever received and learned from their own experiences.\n\nOlayemi, Businesswoman/ Fashion stylist\n\nFirstly, before you invest make sure you have an emergency fund so you won’t be forced to liquidate your investment when an emergency occurs. Outside the emergency fund, have a savings account and from the savings take out money for investment.\n\nInvestments are for the long term so be sure you are comfortable enough to allow the money set aside for it to grow and multiply over the years while you also add to it. Secondly, invest in foreign currency to hedge against naira devaluation.\n\nYusuf, Head, structuring, and Origination at AFEX\n\nThat would be, you put your money only in investments that you understand and can distinguish how the investments work.\n\nTaiwo, Financial Analyst\n\nOnly invest in something you understand. If the returns are ridiculously or not logically explained, run.\n\nMohammed, Senior Product Manager\n\nThe best advice I have learned is to never forget the market knows better than me. A lot of smart people fall for the trap of overestimating how smart they are and because of that, they think they know better than everyone else. At the bottom of it, a market is a place where buyers and sellers come together, and the market (the collection of all these buyers and sellers communicate through price and other data like trade volume, etc). Therefore, if the market is saying something through all those numbers, it’s important to not think you know better than the mark",
        }
        res = self.client.post(CREATE_BLOG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        blog = BlogArticle.objects.get(**res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_blog_success(self):
        """Test Retrieving"""
