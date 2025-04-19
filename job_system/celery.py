from __future__ import absolute_import
import os
from celery import Celery

# Set the default Django settings module for the 'celery' command-line program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_system.settings")

app = Celery("job_system")

# Load task modules from all registered Django app configs.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
