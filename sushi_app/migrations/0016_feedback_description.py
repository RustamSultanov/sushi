# Generated by Django 2.2.3 on 2019-07-28 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0015_auto_20190728_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]