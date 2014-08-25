
from __future__ import absolute_import
from celery import Celery
import os

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiral.settings')

app = Celery('spiral',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['apps.sp.tasks'])

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
    CELERY_TASK_RESULT_EXPIRES=3600,
    BROKER_URL='redis://localhost:6379/0'
)

CELERY_TIMEZONE = 'UTC'

if __name__ == '__main__':
    app.start()

try:
    import djcelery
    djcelery.setup_loader()

    BROKER_URL = 'redis://localhost:6379/0'

    CELERYD_LOG_COLOR = False ### turns the output colors to black.
    CELERY_IMPORTS = ('apps.sp.tasks',) ### specify the route of the tasks file.
    CELERY_ALWAYS_EAGER = True ### True for development mode, so the process are executed locally.
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

    from local_settings import *

except ImportError:
    pass

#Execute: python manage.py celeryd -B -l DEBUG