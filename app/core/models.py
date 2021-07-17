from django.db import models
from django_celery_results.models import TaskResult
from django.utils.functional import cached_property


class Task(models.Model):
    task_result = models.ForeignKey(TaskResult, related_name='+', on_delete=models.SET_NULL, null=True)
    lock = models.BooleanField(default=False)

    @cached_property
    def key_composer(self):
        return "%s-%s" % (
            self.__class__.__name__.lower(),
            self.id
        )

    def get_context(self):
        return {
            'links': [url.link for url in self.url_set.all()]
        }


class Url(models.Model):
    link = models.URLField()
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
