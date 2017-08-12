# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='display_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]