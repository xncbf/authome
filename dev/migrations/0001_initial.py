# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-16 12:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Macro',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='매크로명')),
                ('detail', models.TextField()),
                ('fee', models.IntegerField(default=0, verbose_name='가격')),
                ('auth_date', models.IntegerField(default=30, verbose_name='추가일자')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '매크로',
            },
        ),
        migrations.CreateModel(
            name='MacroFeeLog',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('macro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev.Macro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '결제로그',
            },
        ),
        migrations.CreateModel(
            name='MacroLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField()),
                ('macro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev.Macro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '사용로그',
            },
        ),
        migrations.CreateModel(
            name='UserPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField(verbose_name='종료일')),
                ('macro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev.Macro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '인증정보',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userpage',
            unique_together=set([('user', 'macro')]),
        ),
    ]
