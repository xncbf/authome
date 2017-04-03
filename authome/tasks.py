from django.core.management import call_command
from django.utils import timezone
from authome.celery import app
from main.models import UserPage


@app.task
def get_ses_statistics():
    call_command('get_ses_statistics')


def verify_end_yn():
    UserPage.objects.filter(end_date__lt=timezone.now()).update(end_yn=False)
