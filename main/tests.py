from django.test import TestCase
from django.core import mail
from django.test.utils import override_settings


@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class SmtpTests(TestCase):
    def test_send_email(self):
        mail_sent_success = mail.send_mail('Subject here', 'Here is the message.', '', ['xncbf12@gmail.com'], fail_silently=False)
        self.assertEquals(mail_sent_success, 1)
