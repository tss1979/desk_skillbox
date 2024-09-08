import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_3_am': {
        'task': 'desk.tasks.clear_table_one_code',
        'schedule': crontab(hour='3', minute='0', day_of_week='monday'),
    },
}