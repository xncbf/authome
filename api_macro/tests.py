from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from main.models import Macro, UserPage


class Tests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(email="xncbf12@gmail.com")
        macro = Macro.objects.create(user=user)
        UserPage.objects.create(user=user, macro=macro, end_date=timezone.now() + timedelta(days=1))

    def test_success_request(self):
        testing_account = User.objects.get(email='xncbf12@gmail.com')
        token = testing_account.extendsuser.token
        macro_id = Macro.objects.get(user=testing_account).id
        response = self.client.get('/macro/auth/%s/%s/' % (str(token), macro_id))
        self.assertEqual(response.status_code, 200)
