from django.test import TestCase


class Tests(TestCase):
    def test_success_request(self):
        # Using the standard RequestFactory API to create a form POST request
        response = self.client.get(
            '/macro/auth/b9ea35f6-3f78-4f82-9136-f740b3bfab3c/fd7fbf5a-2840-49df-a235-74ed9877a1a2/')
        self.assertEqual(response.status_code, 200)
