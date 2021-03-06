# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-09-18 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


def update_expired_date(apps, schema_editor):
    Menu = apps.get_model('menu', 'Menu')
    for menu in Menu.objects.all():
        try:
            menu.expiration_date = datetime.datetime.strftime(menu.expiration_date, "%Y-%m-%d")
        except TypeError:
            menu.expiration_date = None
        menu.save()


class Migration(migrations.Migration):
    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', to='menu.Ingredient'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateField(blank=True, help_text='MM/DD/YYYY', null=True),
        ),
        migrations.RunPython(update_expired_date),
    ]
