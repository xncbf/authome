from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APITestCase, RequestsClient


from main.models import Macro, UserPage


class Tests(TestCase):
    def setUp(self):
        # self.site = Site(
        #     id=settings.SITE_ID,
        #     domain="example.com",
        #     name="example.com",
        # )
        # self.site.save()
        user = User.objects.create(email="xncbf12@gmail.com")
        macro = Macro.objects.create(user=user)
        UserPage.objects.create(user=user, macro=macro, end_date=timezone.now() + timedelta(days=1))

    def test_success_request(self):
        testing_account = User.objects.get(email='xncbf12@gmail.com')
        token = testing_account.extendsuser.token
        macro_id = Macro.objects.get(user=testing_account).id

        response = self.client.get('/macro/auth/%s/%s/' % (str(token), macro_id))

        print(response)
        self.assertEqual(response.status_code, 200)
