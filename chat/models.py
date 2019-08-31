from django.db import models

from django.conf import settings


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