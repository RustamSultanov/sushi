from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class IdeaModel(models.Model):
    """docstring for IdeaModel"""

    ST_CONSIDERATION, ST_OK, ST_REJECTED = range(3)
    STATUS_CHOICE = (
        (ST_CONSIDERATION, "На рассмотрении"),
        (ST_OK, "Одобрено"),
        (ST_REJECTED, "Отклонено"),
    )

    email = models.EmailField(blank=False, null=False, verbose_name='Email')
    phone_number = PhoneNumberField(null=False, blank=False,
                                    verbose_name='Номер телефона')    
    body = models.CharField(max_length=1000, blank=False, null=False,
                            verbose_name='Сообщение')
    status = models.IntegerField(choices=STATUS_CHOICE, default=ST_CONSIDERATION)
    answer = models.CharField(max_length=1000, blank=False, null=False,
                              verbose_name='Ответ')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_answer = models.DateTimeField(auto_now_add=True, verbose_name='Дата оповещения автора')

    class Meta:
        verbose_name = 'Идея от пользователя'
        verbose_name_plural = 'Идеи от пользоватлей'
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.body} от {self.email}'
