# Generated by Django 2.2.2 on 2019-07-18 16:56

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0008_auto_20190718_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionmodel',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона'),
        ),
    ]