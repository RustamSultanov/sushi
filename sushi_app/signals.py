from .models import *


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
        status = 'new' if kwargs['created'] else 'updated'
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


@receiver(post_save, sender=IdeaModel)
@register_event_type(IDEA_T)
def handle_idea(instance, event_type, **kwargs):
    fin = [instance.recipient]
    subs = Subscribes.objects.filter(event_type=event_type, user_id__in=fin)
    if kwargs['created']:
        return

    for sub in subs:
        status = ''
        if instance.status == IdeaModel.ST_OK:
            status = 'accepted'
        elif instance.status == IdeaModel.ST_REJECTED:
            status = 'rejected'
        else:
            return

        event = NotificationEvents(event_id=instance.pk,
                                   event_type=event_type,
                                   subscribe=sub,
                                   value=status)
        event.save()


@receiver(post_save, sender=NewsPage)
@register_event_type(NEWS_T)
def handle_news(instance, event_type):
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
def handle_materials(instance, event_type):
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
