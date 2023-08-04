import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'simpleapp.task.mailing', 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

app.conf.beat_schedule = {'action_every_hour': {'task': 'simplespp.tasks.notify', 'schedule': 3600, }, }
