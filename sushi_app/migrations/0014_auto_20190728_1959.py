# Generated by Django 2.2.3 on 2019-07-28 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sushi_app', '0013_auto_20190722_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='adv',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='disadv',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='files',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='product',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='text',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='user',
        ),
        migrations.AddField(
            model_name='feedback',
            name='manager',
            field=models.ForeignKey(default=1, limit_choices_to={'is_manager': True}, on_delete=django.db.models.deletion.CASCADE, related_name='feed_manager', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='responsible',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='feed_responsible', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sushi_app.Shop'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Решен'), (1, 'Обрабатывается'), (2, 'Не решен')], default=1),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Решен'), (1, 'Обрабатывается'), (2, 'Не решен')], default=1)),
                ('manager', models.ForeignKey(limit_choices_to={'is_manager': True}, on_delete=django.db.models.deletion.CASCADE, related_name='task_manager', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_responsible', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Решен'), (1, 'Обрабатывается'), (2, 'Не решен')], default=1)),
                ('manager', models.ForeignKey(limit_choices_to={'is_manager': True}, on_delete=django.db.models.deletion.CASCADE, related_name='requests_manager', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_responsible', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
