import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("reminders")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.worker_hijack_root_logger = False

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
