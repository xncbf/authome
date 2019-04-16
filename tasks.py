from django.utils import timezone
from dev.models import UserPage


def verify_end_yn():
    UserPage.objects.filter(end_date__lt=timezone.now()).update(end_yn=False, is_active=False)
    UserPage.objects.filter(end_date__gte=timezone.now()).update(end_yn=True, is_active=True)
