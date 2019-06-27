from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from audiofield.models import AudioFile
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class UserManager(BaseUserManager):
	"""
	A custom user manager to deal with emails as unique identifiers for auth
	instead of usernames. The default that's used is "UserManager"
	"""
	def create_user(self, phone_number, profile_picture=None, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not phone_number:
		    raise ValueError('Users must have an phone number')

		user = self.model(
		    phone_number=phone_number,
		    profile_picture=profile_picture,
		    username =phone_number,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
		    phone_number,
		    password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    profile_picture = models.ImageField(
        upload_to='user_data/profile_picture', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    

    def __str__(self):
        return f'{self.phone_number}'

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.phone_number

    def get_username(self):
        return f'{self.phone_number}'

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
