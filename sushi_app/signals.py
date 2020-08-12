from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .enums import * 
from mickroservices.models import NewsPage, IdeaModel


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
    if fin[0] != instance.manager.user:
        fin.append(instance.manager.user)
    
    subs = Subscribes.objects.filter(event_type=event_type,
                                     user_id__in=fin)
    for sub in subs:
        status = 'new' if kwargs['created'] else 'updated'
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub, 
                                   value=status)
        event.save()


@receiver(post_save, sender=Feedback)
@register_event_type(FEEDBACK_T)
def handle_feedback(instance, event_type, **kwargs):
    fin = [instance.responsible.user]
    if fin[0] != instance.manager.user:
        fin.append(instance.manager.user)
    
    subs = Subscribes.objects.filter(event_type=event_type,
                                     user_id__in=fin)
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
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub)

        event.save()


@receiver(post_save, sender=Shop)
@register_event_type(SHOP_T)
def handle_shop(instance, event_type, **kwargs):
    fin = [instance.partner.user, *[i.user for i in instance.responsibles.all()]]
    subs = Subscribes.objects.filter(event_type=event_type)
    for sub in subs:
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub)

        event.save()



@receiver(post_save, sender=IdeaModel)
@register_event_type(IDEA_T)
def handle_idea(instance, event_type, **kwargs):
    fin = [instance.recipient]
    subs = Subscribes.objects.filter(event_type=event_type)
    for sub in subs:
        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub)

        event.save()

