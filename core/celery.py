import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery('core', broker=settings.CELERY_BROKER_URL)

app.conf.enable_utc = False
app.conf.update(timezone='Europe/Istanbul')

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(settings.INSTALLED_APPS)
