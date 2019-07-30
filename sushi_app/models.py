from django.db import models
from django.contrib.auth.models import AbstractUser
from wagtail.documents.models import Document, AbstractDocument
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from wagtail.core.fields import RichTextField
from wagtail.documents.models import get_document_model
import wagtail.users.models

ST_SOLVED, ST_IN_PROGRESS, ST_NOT_SOLVED = range(3)
STATUS_CHOICE = (
    (ST_SOLVED, "Решен"),
    (ST_IN_PROGRESS, "Обрабатывается"),
    (ST_NOT_SOLVED, "Не решен"),
)


class Department(models.Model):
    name = models.CharField(max_length=256, db_index=True)

    def __str__(self):
        return f"{self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile'
    )
    wagtail_profile = models.OneToOneField(
        wagtail.users.models.UserProfile, on_delete=models.CASCADE, related_name='user_profile',
        null=True, blank=True
    )
    position = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True, blank=True)
    whatsapp = PhoneNumberField(null=True, blank=True)
    twitter = models.URLField(null=True, max_length=200, blank=True)
    facebook = models.URLField(null=True, max_length=200, blank=True)
    instagram = models.URLField(null=True, max_length=200, blank=True)
    key_responsibilities = RichTextField(blank=True)
    is_partner = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_head = models.BooleanField(blank=True, default=False)
    manager = models.ForeignKey(on_delete=models.SET_NULL, to='self', related_name='partner',
                                null=True, blank=True, limit_choices_to={'is_manager': True})
    head = models.ForeignKey(on_delete=models.SET_NULL, to='self', related_name='employee',
                             null=True, blank=True, limit_choices_to={'is_head': True})
    department = models.ForeignKey(on_delete=models.SET_NULL, to=Department, related_name='member',
                                   null=True, blank=True)

    def __str__(self):
        return self.user.get_username()


class Task(models.Model):
    responsible = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL,
                                              related_name='task_responsible')
    manager = models.ForeignKey(on_delete=models.CASCADE, to=UserProfile, related_name='task_manager',
                                limit_choices_to={'is_manager': True})
    title = models.CharField(max_length=256)
    description = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=ST_IN_PROGRESS)

    def __str__(self):
        return f"{self.date_create}, {self.status}"


class Requests(models.Model):
    responsible = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL,
                                              related_name='requests_responsible')
    manager = models.ForeignKey(on_delete=models.CASCADE, to=UserProfile, related_name='requests_manager',
                                limit_choices_to={'is_manager': True})
    title = models.CharField(max_length=256)
    description = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=ST_IN_PROGRESS)

    def __str__(self):
        return f"{self.date_create}, {self.status}"


class Shop(models.Model):
    address = models.CharField(max_length=255, blank=False, null=False,
                               verbose_name='Адрес магазина')
    docs = models.ManyToManyField(
        get_document_model(),
        blank=True,
        related_name='+'
    )
    checks = models.ManyToManyField(
        get_document_model(),
        blank=True,
        related_name='+'
    )
    partner = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}"

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Product(models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='user')
    title = models.CharField(max_length=256)
    short_descrip = models.CharField(max_length=256)
    descrip = models.TextField()
    composition = models.TextField()
    characteristics = models.TextField()
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    RATING_CHOICE = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    )
    rating = models.IntegerField(choices=RATING_CHOICE, default=5)
    files = models.ImageField(blank=True)

    def __str__(self):
        return f" {self.title}, дата: {self.date_create}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Feedback(models.Model):
    responsible = models.ForeignKey(on_delete=models.CASCADE, to=UserProfile,
                                              related_name='feed_responsible')
    manager = models.ForeignKey(on_delete=models.CASCADE, to=UserProfile, related_name='feed_manager',
                                limit_choices_to={'is_manager': True})
    shop = models.ForeignKey(on_delete=models.CASCADE, to=Shop)
    date_create = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=ST_IN_PROGRESS)
    description = models.TextField()

    def __str__(self):
        return f"{self.date_create}, {self.status}"


class Messeges(models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='user_messeges')
    accepter = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='accepter')
    product = models.ForeignKey(on_delete=models.CASCADE, to=Product, blank=True, null=True)
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.date_create}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
