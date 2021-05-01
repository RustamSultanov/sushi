from django.db import models
import sushi_app.models
from django.conf import settings
# from mickroservices.models import QuestionModel, IdeaModel


class Room(models.model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

class Message(models.Model):
    STATUS = (('new', 'Непрочитано'), ('read', 'Прочитано'))
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=10, choices=STATUS,
                              default='new')
    text = models.TextField('Текст', null=True, blank=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField('Файл', null=True, blank=True)




class Message1(models.Model):
    ST_WAITNG, ST_READING = range(2)
    STATUS_CHOICE = (
        (ST_WAITNG, 'в ожидании'),
        (ST_READING, 'прочтена'),
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sender_messages')
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipient_messages')
    body = models.TextField('body message')
    status = models.SmallIntegerField(
        choices=STATUS_CHOICE,
        default=ST_WAITNG
    )
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(on_delete=models.CASCADE, to=sushi_app.models.Task, blank=True, null=True)
    requests = models.ForeignKey(on_delete=models.CASCADE, to=sushi_app.models.Requests, blank=True, null=True)
    feedback = models.ForeignKey(on_delete=models.CASCADE, to=sushi_app.models.Feedback, blank=True, null=True)
    idea = models.ForeignKey(on_delete=models.CASCADE, to=IdeaModel, blank=True, null=True)
    question = models.ForeignKey(on_delete=models.CASCADE, to=QuestionModel, blank=True, null=True)
