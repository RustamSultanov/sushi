from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class Product(models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='user')
    title = models.CharField(max_length=256)
    short_descrip = models.CharField(max_length=256)
    descrip = models.TextField()
    composition = models.TextField()
    characteristics = models.TextField()
    date_update = models.DateTimeField(auto_now=True,blank=True,null=True)
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
    user = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='user_feed',blank=True,null=True)
    product = models.ForeignKey(on_delete=models.CASCADE,to=Product)
    text = models.TextField()
    adv = models.TextField()
    disadv = models.TextField()
    files = models.FileField(blank=True,null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    RATING_CHOICE = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    )
    rating = models.IntegerField(choices=RATING_CHOICE, default=5)
    def __str__(self):
        return f"{self.date_create}"

class Messeges(models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='user_messeges')
    accepter = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='accepter')
    product = models.ForeignKey(on_delete=models.CASCADE,to=Product,blank=True,null=True)
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.date_create}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
