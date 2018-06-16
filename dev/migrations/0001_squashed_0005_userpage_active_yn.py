# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-16 14:51
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    replaces = [('dev', '0001_squashed_0002_auto_20180117_2311'), ('dev', '0002_auto_20180117_2354'),
                ('dev', '0003_auto_20180118_0212'), ('dev', '0004_auto_20180615_1644'),
                ('dev', '0005_userpage_active_yn')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '매크로',
                'db_table': 'main_macro',
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
                'db_table': 'main_macrofeelog',
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
                ('succeeded', models.NullBooleanField()),
            ],
            options={
                'verbose_name_plural': '사용로그',
                'db_table': 'main_macrolog',
            },
        ),
        migrations.CreateModel(
            name='UserPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='종료일')),
                ('end_yn', models.BooleanField(default=True)),
                ('macro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev.Macro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '인증정보',
                'db_table': 'main_userpage',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userpage',
            unique_together=set([('user', 'macro')]),
        ),
        migrations.AlterField(
            model_name='macro',
            name='title',
            field=models.CharField(max_length=30, verbose_name='매크로명'),
        ),
        migrations.CreateModel(
            name='board',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=70, verbose_name='제목')),
                ('detail', models.TextField(verbose_name='내용')),
                ('ip', models.GenericIPAddressField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.CharField(max_length=50, verbose_name='카테고리')),
                ('display', models.BooleanField(default=True, verbose_name='표시')),
                ('removed', models.BooleanField(default=False, verbose_name='삭제')),
            ],
            options={
                'verbose_name_plural': '게시판',
                'ordering': ['-created'],
                'db_table': 'main_board',
            },
        ),
        migrations.AlterField(
            model_name='macro',
            name='detail',
            field=models.TextField(verbose_name='간단한 설명'),
        ),
        migrations.CreateModel(
            name='ExtendsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nickname', models.CharField(error_messages={'unique': '이미 사용중인 닉네임입니다.'},
                                              help_text='필수 항목. 10자 이하. 문자와 숫자만 가능.',
                                              max_length=10, null=True,
                                              unique=True,
                                              validators=[
                                                  django.core.validators.RegexValidator('^[\\w]+$',
                                                                                        '유효한 닉네임을 입력해주세요. '
                                                                                        '이 항목은® 문자와 숫자만 사용 '
                                                                                        '가능합니다.')],
                                              verbose_name='닉네임')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extendsuser',
                                              to=settings.AUTH_USER_MODEL)),
                ('nickname_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'main_extendsuser',
            },
        ),
        migrations.AddField(
            model_name='userpage',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
