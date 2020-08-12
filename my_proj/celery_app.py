import os  
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange, binding


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_proj.settings')
app = Celery('celery_app')  
app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks()  

normal_ex = Exchange('normal', type='direct')
low_ex = Exchange('low', type='direct')

app.conf.update(
    task_queues = (
        Queue('normal', normal_ex, routing_key='normal'),
        Queue('low', low_ex, routing_key='low'),
    ),
    task_default_exchange = 'my_proj.normal',
    task_default_queue = 'my_proj.normal'
)

app.conf.update(
    task_routes=  {
        'plugin.email.tasks.bulk_event_mailing': {'queue': 'normal'},
    }
)

app.conf.beat_schedule = {
    'bulk-email-send': {
        'task': 'sushi_app.tasks.bulk_event_mailing',
        'schedule': 5,
        'options': {'queue' : 'low', 'routing_key': 'low'}
    }
}

