# Generated by Django 2.2.14 on 2020-12-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0044_auto_20201025_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий к пользователю'),
        ),
    ]
