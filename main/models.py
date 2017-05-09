import uuid
import os

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core import validators
from django.utils import timezone
from hitcount.models import HitCount, HitCountMixin


class TimeStampedModel(models.Model):
    """
    create 와 modified 필드를 자동으로 업데이트해 주는
     추상화기반 클래스모델
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Macro(TimeStampedModel):
    """
    등록된 매크로 정보를 저장
    """
    class Meta:
        verbose_name_plural = '매크로'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('매크로명', max_length=30)
    detail = models.TextField('간단한 설명')
    user = models.ForeignKey(User)
    # fee = models.IntegerField('가격', default=0)
    # auth_date = models.IntegerField('추가일자', default=30)

    def __str__(self):
        return "%s" % self.title


class MacroFeeLog(TimeStampedModel):
    """
    유저의 매크로 결제 내역을 저장
    """
    class Meta:
        verbose_name_plural = '결제로그'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)


class MacroLog(TimeStampedModel):
    """
    매크로 사용 로그를 저장
    """
    class Meta:
        verbose_name_plural = '사용로그'
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    ip = models.GenericIPAddressField()
    succeded = models.NullBooleanField()


class UserPage(TimeStampedModel):
    """
    유저의 인증정보를 저장
    """
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    end_date = models.DateTimeField('종료일', default=timezone.now)
    # 의미가 뒤바뀜 활성화 YN으로 생각하자 ㅠㅠ(True 가 활성)
    end_yn = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = '인증정보'
        unique_together = (("user", "macro"), )

    def __str__(self):
        return "%s" % self.user

    @property
    def is_past_due(self):
        return timezone.now() > self.end_date


class Board(TimeStampedModel, HitCountMixin):
    """
    게시글의 정보를 저장
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField('제목', max_length=70, null=False)
    detail = models.TextField('내용')
    user = models.ForeignKey(User)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')
    ip = models.GenericIPAddressField()

    class Meta:
        verbose_name_plural = '게시판'


# class CustomUserManager(BaseUserManager):
#     def uuid_renewal(self):
#         if self.count() == 1:
#             return self.update_or_create(token=uuid.uuid4())
#         else:
#             raise ValueError("하나의 대상만 업데이트하세요.")


class ExtendsUser(models.Model):
    """
    유저 모델 확장
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    nickname = models.CharField(
        '닉네임',
        max_length=10,
        unique=True,
        help_text='필수 항목. 10자 이하. 문자와 숫자만 가능.',
        validators=[
            validators.RegexValidator(
                r'^[\w]+$',
                '유효한 닉네임을 입력해주세요. 이 항목은 '
                '문자와 숫자만 사용 가능합니다.'
            ),
        ],
        error_messages={
            'unique': "이미 사용중인 닉네임입니다.",
        },
        null=True,
    )


class CustomUser(User):
    class Meta:
        proxy = True

    def _make_new_uuid(self):
        ExtendsUser.objects.create(user=self)

    def make_new_uuid(self):
        self._make_new_uuid()

    def save(self, *args, **kwargs):
        # do anything you need before saving
        super(CustomUser, self).save(*args, **kwargs)
        self.make_new_uuid()
        # do anything you need after saving
