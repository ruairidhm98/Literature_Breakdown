# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 19:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lit', '0021_auto_20180319_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='title',
        ),
        migrations.DeleteModel(
            name='Snippet',
        ),
    ]
