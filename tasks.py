from django.utils import timezone
from dev.models import UserPage


def verify_end_yn():
    UserPage.objects.filter(end_date__lt=timezone.now(), end_yn=True).update(end_yn=False)
    UserPage.objects.filter(end_date__gte=timezone.now(), end_yn=False).update(end_yn=True)
