# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 18:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('cancelled', models.BooleanField()),
                ('comment', models.CharField(max_length=500)),
                ('receiver_type', models.CharField(choices=[('twitter', 'Twitter'), ('vk', 'VK'), ('email', 'Email')], max_length=10)),
                ('receiver', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('comment', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('local_id', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('last_reward', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transfer',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='app.Wallet'),
        ),
        migrations.AddField(
            model_name='transfer',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='app.Wallet'),
        ),
        migrations.AddField(
            model_name='pendingtransfer',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Wallet'),
        ),
    ]
