# Generated by Django 2.2.3 on 2019-08-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0012_auto_20190818_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentsushi',
            name='doc_type',
            field=models.IntegerField(choices=[(0, 'Техкарты'), (1, 'Регламенты'), (2, 'Акции'), (3, 'Перед открытием'), (4, 'Меню'), (5, 'Другие макеты'), (6, 'Видеоролики'), (7, 'Аудиоролики')], default=0),
        ),
    ]