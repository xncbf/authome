from __future__ import absolute_import

from celery import Celery


# djano 에서 쓰일 setting 지정 아래의 경우 proj/settings.py 를 사용한다는 뜻
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authome.settings')
from django.conf import settings  # noqa

# app = Celery('proj',
#              broker='amqp://guest@localhost//',
#              backend='amqp://',
#              include=['proj.tasks'])

app = Celery('authome')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#
# app.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )

if __name__ == '__main__':
    app.start()
