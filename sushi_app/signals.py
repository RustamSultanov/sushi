from django.db.models.signals import post_save
from django.dispatch import receiver

from mickroservices.models import IdeaModel, NewsPage, DocumentSushi, QuestionModel
from mickroservices.utils import generate_doc_preview

from sushi_app.enums import MATERIALS_T, NEWS_T, IDEA_T, SHOP_T, MESSEGE_T, FEEDBACK_T, TASK_T
from sushi_app.models import NotificationEvents, Subscribes, Shop, Messeges, Feedback, Task, Requests, REQUEST_T, \
    QUESTION_T


def register_event_type(event_type):
    def deco(func):
        def wrapper(*args, **kwargs):
            return func(*args, event_type=event_type, **kwargs)

        return wrapper

    return deco


@receiver(post_save, sender=Task)
@register_event_type(TASK_T)
def handle_task(instance, event_type, **kwargs):
    fin = [instance.responsible]
    subs = Subscribes.objects.filter(event_type=event_type,
                                     user_id__in=fin)
    for sub in subs:
        status = 'new' if kwargs['created'] else 'updated'
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=Requests)
@register_event_type(REQUEST_T)
def handle_request(instance, event_type, **kwargs):
    status = 'new' if kwargs['created'] else 'updated'
    if status == 'new':
        recepient = instance.manager.user
    else:
        recepient = instance.responsible
        
    subs = Subscribes.objects.filter(event_type=event_type,
                                     user_id=recepient)
    for sub in subs:
        
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=Feedback)
@register_event_type(FEEDBACK_T)
def handle_feedback(instance, event_type, **kwargs):
    try:
        is_responsible_request = instance._request_user == instance.responsible.user  
        if is_responsible_request:
            recepient =  instance.manager.user
    except AttributeError:
        recepient = instance.responsible.user

    subs = Subscribes.objects.filter(event_type=event_type,
                                     user_id=recepient)
    for sub in subs:
        status = 'new' if kwargs['created'] else 'updated'
            
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=Messeges)
@register_event_type(MESSEGE_T)
def handle_messeges(instance, event_type, **kwargs):
    fin = [instance.to_user]
    subs = Subscribes.objects.filter(event_type=event_type,
                                     user_id__in=fin)
    for sub in subs:
        status = 'new' if kwargs['created'] else 'updated'
        if instance.feedback:
            status = 'feedback_updated'

        if instance.requests:
            status = 'request_updated'

        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=Shop)
@register_event_type(SHOP_T)
def handle_shop(instance, event_type, **kwargs):
    fin = [instance.partner.user, *[i.user for i in instance.responsibles.all()]]
    subs = Subscribes.objects.filter(event_type=event_type, user_id__in=fin)
    for sub in subs:
        status = 'new' if kwargs['created'] else 'updated'
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


IDEA_UPDATE_STATUSES = {
    IdeaModel.ST_OK: 'accepted',
    IdeaModel.ST_REJECTED: 'rejected'
}


@receiver(post_save, sender=IdeaModel)
@register_event_type(IDEA_T)
def handle_idea(instance, event_type, **kwargs):
    sub = Subscribes.objects.filter(event_type=event_type)

    if instance.status in IDEA_UPDATE_STATUSES:
        status = IDEA_UPDATE_STATUSES[instance.status]
        sub = sub.filter(user_id=instance.sender).first()
    else:
        sub = sub.filter(user_id=instance.recipient).first()
        status = 'new'

    if sub:
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=NewsPage)
@register_event_type(NEWS_T)
def handle_news(instance, event_type,**kwargs):
    first = NotificationEvents.objects.filter(event_type=event_type,
                                              event_id=instance.pk) \
        .order_by('date_of_creation').first()
    if first:
        date = first.date_of_creation
        from django.utils import timezone
        cur_time = timezone.now()
        if (cur_time - date).seconds < 10:
            return

    subs = Subscribes.objects.filter(event_type=event_type)

    for sub in subs:
        status = 'updated' if first else 'new'
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@register_event_type(MATERIALS_T)
def handle_materials(instance, event_type,**kwargs):
    shops = Shop.objects.filter(docs__id=instance.pk)
    if shops:
        subscribers = set()
        for shop in shops:
            subscribers.add(shop.partner.user.pk)
            for resp in shop.responsibles.all():
                subscribers.add(resp.user.pk)

        subs = Subscribes.objects.filter(event_type=event_type,
                                         user_id__in=subscribers)

        for sub in subs:
            status = 'new'
            event = NotificationEvents(event_id=instance.pk,
                                       event_type=event_type,
                                       subscribe=sub,
                                       value=status)
            event.save()


QUESTION_UPDATE_STATUSES = {
    QuestionModel.ST_OK: 'accepted',
    QuestionModel.ST_REJECTED: 'rejected'
}


@receiver(post_save, sender=QuestionModel)
@register_event_type(QUESTION_T)
def handle_question(instance, event_type, **kwargs):
    sub = Subscribes.objects.filter(event_type=event_type)

    if instance.status in QUESTION_UPDATE_STATUSES:
        if instance._old_answer != instance.answer and instance._old_answer:
            status = 'updated'
        else:
            status = 'accepted'
        sub = sub.filter(user_id=instance.user).first()
    else:
        manager = instance.user.user_profile.manager.user
        sub = sub.filter(user_id=manager).first()
        status = 'new'

    if sub:
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=DocumentSushi)
def generate_preview(instance, **kwargs):
    generate_doc_preview(instance)
