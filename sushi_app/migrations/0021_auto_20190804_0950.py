# Generated by Django 2.2.3 on 2019-08-04 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0020_auto_20190804_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='scan',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
