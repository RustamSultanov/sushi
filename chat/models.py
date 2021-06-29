from django.db import models
import sushi_app.models
from django.conf import settings
from mickroservices.models import QuestionModel, IdeaModel


from django import forms

class Room(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    name = models.CharField(max_length=120, default="Group")
    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id

class ChatMessageFile(models.Model):
    name = models.CharField("Имя файла", max_length=120)
    file = models.FileField('Файл',upload_to='chat/', null=True, blank=True)

    def url(self):
        return self.file.url

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    STATUS = (('new', 'Непрочитано'), ('read', 'Прочитано'))
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=10, choices=STATUS,
                              default='new')
    text = models.TextField('Текст', null=True, blank=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(ChatMessageFile, on_delete=models.CASCADE, null=True, blank=True)

    def change_status(self):
        self.status = 'read'
        self.save()

class Message(models.Model):
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
