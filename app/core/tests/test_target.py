import json
from celery.contrib.testing.worker import start_worker
from django.test import SimpleTestCase
from app.core.models import Task
from app.core.tasks import app, run_script


class WorkerTest(SimpleTestCase):
    celery_worker = None
    databases = '__all__'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    @classmethod
    def test_run_script(cls):
        task, _ = Task.objects.get_or_create()
        run_script.delay(
            json.dumps({
                'links': ['https://alexis-le-baron.com/en/']
            }),
            task.id)
