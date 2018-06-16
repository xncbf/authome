from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase, APIRequestFactory

from dev.models import Macro, UserPage
from .views import GetAuth2


class Tests(APITestCase):
    def setUp(self):
        user = User.objects.create(email="xncbf12@gmail.com")
        macro = Macro.objects.create(user=user)
        self.time = timezone.now() + timedelta(days=1)
        UserPage.objects.create(user=user, macro=macro, end_date=self.time)

    def test_success_request(self):
        testing_account = User.objects.get(email='xncbf12@gmail.com')
        token = testing_account.extendsuser.token
        macro_id = Macro.objects.get(user=testing_account).id

        factory = APIRequestFactory()
        view = GetAuth2.as_view()
        request = factory.get('/')
        response = view(request, token=str(token), macro_id=macro_id)
        self.assertEqual(response.data.get('is_active'), True)
