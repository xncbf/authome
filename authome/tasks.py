from django.core.management import call_command
from django.utils import timezone
from main.models import UserPage


@app.task
def get_ses_statistics():
    call_command('get_ses_statistics')


@app.task
def verify_end_yn():
    UserPage.objects.filter(end_date__lt=timezone.now(), end_yn=True).update(end_yn=False)
    UserPage.objects.filter(end_date__gte=timezone.now(), end_yn=False).update(end_yn=True)
