from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from _datetime import timedelta
import uuid


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
    title = models.CharField('매크로명', max_length=50)
    detail = models.TextField()
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

    def __str__(self):
        return "%s / %s / %s" % (self.user, self.macro, self.create_date)


class MacroLog(TimeStampedModel):
    """
    매크로 사용 로그를 저장
    """
    class Meta:
        verbose_name_plural = '사용로그'
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return "%s : %s " % (self.user, self.ip)


class UserPage(TimeStampedModel):
    """
    유저의 인증정보를 저장
    """
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    end_date = models.DateTimeField('종료일', default=timezone.now)
    end_yn = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = '인증정보'
        unique_together = (("user", "macro"), )

    def __str__(self):
        return "%s" % self.user
