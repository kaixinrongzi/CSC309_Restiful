# from django.contrib.sites import requests
from django.test.client import Client
import requests
from django.test import TestCase


# Create your tests here.
class Test(TestCase):
    def test1(self):
        url = f"http://localhost:8000/accounts/register/"
        data = {"username": "", "password1": "", "password2": "", "email": "", "first_name": "", "last_name": ""}
        self.client = Client()
        res = self.client.post(url, data=data)
        print("res:", res.text)
        # self.assertEqual(res.text.count("This field is required"), 3)

