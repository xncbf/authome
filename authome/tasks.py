from django.core.management import call_command
from authome.celery import app


@app.task
def get_ses_statistics():
    f = open("new.txt", 'w')
    f.close()
    call_command('get_ses_statistics')
