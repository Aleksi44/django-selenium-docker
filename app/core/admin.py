import json
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, Group

from app.core.models import Task, Url
from app.core.tasks import run_script


class UrlTabularInline(admin.TabularInline):
    model = Url


class TaskAdmin(admin.ModelAdmin):
    change_form_template = 'core/task_change_form.html'
    inlines = [UrlTabularInline]
    exclude = ('task_result', 'lock')

    def _change_url(self, obj):
        opts = obj._meta
        obj_url = reverse(
            'admin:%s_%s_change' % (opts.app_label, opts.model_name),
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(obj_url)

    def response_add(self, request, obj, post_url_continue=None):
        return self._change_url(obj)

    def response_change(self, request, obj):
        return self._change_url(obj)

    def save_related(self, request, form, formsets, change):
        super(TaskAdmin, self).save_related(request, form, formsets, change)
        obj = formsets[0].instance
        if obj.lock:
            messages.warning(request, "Task is already running")
        else:
            obj.lock = True
            obj.save()
            run_script.delay(
                json.dumps(obj.get_context()),
                obj.id)


admin.site.register(Task, TaskAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
