# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-27 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_board_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='macrolog',
            name='succeded',
            field=models.NullBooleanField(),
        ),
    ]
