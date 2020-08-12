from my_proj import celery_app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .models import *
from .enums import *
from django.contrib.auth.models import User
from django.conf import settings
from itertools import chain
from mickroservices.utils import send_message
from mickroservices.models import NewsPage, IdeaModel


from django.core.mail import send_mail


def _get_task_context(pk):
    pass

def _get_messege_context(pk):
    pass

def _get_news_context(pk):
    pass

def _get_feedback_context(pk):
    pass

def _get_shop_context(pk):
    pass

def _get_idea_context(pk):
    pass
    

EMAIL_TEMP_DIR_PREFIX = 'notification_emails'
TEMPLATES_MAP = {
    TASK_T: f'{EMAIL_TEMP_DIR_PREFIX}/task.html',
    MESSEGE_T: f'{EMAIL_TEMP_DIR_PREFIX}/messege.html',
    NEWS_T: f'{EMAIL_TEMP_DIR_PREFIX}/news.html',
    FEEDBACK_T: f'{EMAIL_TEMP_DIR_PREFIX}/feedback.html',
    SHOP_T: f'{EMAIL_TEMP_DIR_PREFIX}/shop_created.html',
    IDEA_T: f'{EMAIL_TEMP_DIR_PREFIX}/idea.html',
}

SELECT_CONTEXT_MAP = {
    TASK_T : _get_task_context,
    MESSEGE_T: _get_messege_context,
    NEWS_T: _get_news_context,
    FEEDBACK_T: _get_feedback_context,
    SHOP_T: _get_shop_context,
    IDEA_T: _get_idea_context,
}

MODELS_SELECTOR = {
    TASK_T: Task,
    MESSEGE_T: Messeges,
    NEWS_T: NewsPage,
    FEEDBACK_T: Feedback,
    SHOP_T: Shop,
    IDEA_T: IdeaModel,
}

SUBJECTS = {
    TASK_T: 'Pass',
    MESSEGE_T: 'Pass',
    NEWS_T: 'Pass',
    FEEDBACK_T: 'Pass',
    SHOP_T: 'Pass',
    IDEA_T: 'Pass', 
}


@celery_app.task(time_limit=20)
def send_email(pk, event_type, template, context, email):
    subject = SUBJECTS[event_type]
    success = send_message(template, context, subject, email)
    if success:
        MODELS_SELECTOR[event_type].objects.get(pk=pk).delete()


@celery_app.task(time_limit=300)
def bulk_event_mailing():
    subs = Subscribes.objects.filter(subscribe_type=REALTIME_C)

    for sub in subs.all():
        for event in sub.subscribe_events.all():
            template = TEMPLATES_MAP[event.event_type]
            context = SELECT_CONTEXT_MAP[event.event_type](event.event_id)
            email = event.subscribe.user_id.email
            if email:
                send_email.delay(vent.subscribe.user_id.id, 
                                 event.event_type,
                                 template, 
                                 context,
                                 email)
    
    
