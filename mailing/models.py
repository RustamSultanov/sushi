from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from sushi_app.models import UserProfile
# Create your models here.

class FilesMailing(models.Model):
    file = models.FileField(upload_to='mailing/%Y/%m/%d/',)

    def download_url(self):
        url = reverse('mailing:download_mail_files')
        return "{}?path={}".format(url, self.file.name)

    def __str__(self):
        return self.file.name.split("/")[-1]

class Mailing(models.Model):
    title = models.CharField(max_length=120, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст рассылки")
    files = models.ManyToManyField(FilesMailing, related_name="manyfile", verbose_name="Вложения")
    senders = models.ManyToManyField(UserProfile, related_name="mailings", verbose_name="Получатели")
    to_create = models.ForeignKey(get_user_model(), related_name="mailings", verbose_name="Получатели", on_delete=models.SET_NULL, null=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    def save_files(self,files:list):
        for file in files:
            e = FilesMailing()
            e.file.save(**file)
            e.save()
            self.files.add(e)

    class Meta:
        ordering = ['-pk', ]

    def url(self):
        return reverse('mailing:mailing_view', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title