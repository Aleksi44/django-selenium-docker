import os
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

app = Celery('app.core')
app.config_from_object(settings, namespace='APP')
app.control.purge()
app.autodiscover_tasks()
