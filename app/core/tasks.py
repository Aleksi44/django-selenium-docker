import json
import time
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.core.tasks_app import app

logger = logging.getLogger('app')

INTERVAL = 5 * 60


@app.task(bind=True, max_retries=3)
def run_script(self, context, task_id):
    logger.info('Task start')
    from django_celery_results.models import TaskResult
    from app.core.browser import Browser
    from app.core.models import Task

    task = Task.objects.get(id=task_id)
    task.task_result = TaskResult.objects.get_task(self.request.id)
    task.save()
    browser = Browser()

    try:
        context = json.loads(context)
        channel_layer = get_channel_layer()

        for link in context['links']:
            logger.debug(f"GET {link}")
            browser.get(link)
            async_to_sync(channel_layer.group_send)(
                task.key_composer,
                {
                    'type': 'sync_function',
                    'screenshot_b64': browser.get_screenshot_as_base64()
                }
            )
            time.sleep(3)
        task.lock = False
        task.save()
        browser.quit()
        return "OK"
    except Exception as exc:
        logger.critical(f"Task critical exception {type(exc).__name__} - {exc.args}\nLast url : {browser.current_url}")
        task.lock = False
        task.save()
        browser.quit()
        raise exc
