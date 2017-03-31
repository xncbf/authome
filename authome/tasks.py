from django.core.management import call_command
from authome.celery import app


@app.task
def get_ses_statistics():
    call_command('get_ses_statistics')
