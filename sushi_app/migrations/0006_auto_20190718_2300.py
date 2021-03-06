# Generated by Django 2.2.2 on 2019-07-18 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sushi_app', '0005_shop_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='checks',
            field=models.ManyToManyField(blank=True, related_name='_shop_checks_+', to='wagtaildocs.Document'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='docs',
            field=models.ManyToManyField(blank=True, related_name='_shop_docs_+', to='wagtaildocs.Document'),
        ),
        migrations.DeleteModel(
            name='CustomDocument',
        ),
    ]
