from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Macro(models.Model):
    """
    등록된 매크로 정보를 저장
    """
    class Meta:
        verbose_name_plural = '매크로'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('매크로명', max_length=50)
    user = models.ForeignKey(User)
    fee = models.IntegerField('가격', default=0)
    auth_date = models.IntegerField('추가일자', default=30)

    def __str__(self):
        return "%s" % (self.title)


class MacroFeeLog(models.Model):
    """
    유저의 매크로 결제 내역을 저장
    """
    class Meta:
        verbose_name_plural = '결제로그'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    create_date = models.DateTimeField('결제일', auto_created=True)

    def __str__(self):
        return "%s / %s / %s" % (self.user, self.macro, self.create_date)


class MacroLog(models.Model):
    """
    매크로 사용 로그를 저장
    """
    class Meta:
        verbose_name_plural = '사용로그'
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    create_date = models.DateTimeField('접속일', auto_created=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return "%s : %s " % (self.user, self.ip)


class UserPage(models.Model):
    """
    유저의 인증정보를 저장
    """
    user = models.ForeignKey(User)
    macro = models.ForeignKey(Macro)
    end_date = models.DateTimeField('종료일')

    class Meta:
        verbose_name_plural = '인증정보'
        unique_together = (("user", "macro"), )

    def __str__(self):
        return "%s" % self.user
