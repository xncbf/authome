# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-17 17:12
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180117_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendsuser',
            name='nickname',
            field=models.CharField(error_messages={'unique': '이미 사용중인 닉네임입니다.'}, help_text='필수 항목. 10자 이하. 문자와 숫자만 가능.', max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[\\w]+$', '유효한 닉네임을 입력해주세요. 이 항목은® 문자와 숫자만 사용 가능합니다.')], verbose_name='닉네임'),
        ),
        migrations.AlterField(
            model_name='extendsuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extendsuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
