# Generated by Django 2.2.3 on 2019-07-23 05:32

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0009_auto_20190718_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdeaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('body', models.CharField(max_length=1000, verbose_name='Сообщение')),
                ('status', models.IntegerField(choices=[(0, 'На рассмотрении'), (1, 'Одобрено'), (2, 'Отклонено')], default=0)),
                ('answer', models.CharField(max_length=1000, verbose_name='Ответ')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_answer', models.DateTimeField(auto_now_add=True, verbose_name='Дата оповещения автора')),
            ],
            options={
                'verbose_name': 'Идея от пользователя',
                'verbose_name_plural': 'Идеи от пользоватлей',
                'ordering': ['-date_created'],
            },
        ),
    ]