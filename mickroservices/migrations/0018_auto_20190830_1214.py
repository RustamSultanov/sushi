# Generated by Django 2.2.3 on 2019-08-30 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mickroservices', '0017_subjects_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentsushi',
            name='sub_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='mickroservices.Subjects', verbose_name='тематика'),
        ),
    ]
