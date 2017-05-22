from django import template
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from ipware.ip import is_valid_ip

register = template.Library()


@register.filter(name='truncateip')
def truncate_ip(value):
    result = ''
    if is_valid_ip(value):
        result = ".".join(value.split('.')[:-1])
        result += ".xxx"
    else:
        result = '유효하지 않은 아이피입니다.'
    return result


@register.filter(name='naturaltime_newly')
def natural_time_newly(value):
    # 오늘로부터 하루 이상 지난 조건
    if (timezone.now() - value).days >= 1:
        return value
    else:
        return naturaltime(value)


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)
