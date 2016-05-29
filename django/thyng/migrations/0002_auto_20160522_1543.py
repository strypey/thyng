# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 15:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thyng', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[(b'user', 'Member'), (b'admin', 'Admin')], max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectmember',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thyng.Project'),
        ),
        migrations.AddField(
            model_name='projectmember',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]