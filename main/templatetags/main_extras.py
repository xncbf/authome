from django import template
from ..models import ExtendsUser
register = template.Library()


@register.filter
def get_or_create_token(user):
    try:
        result = user.extendsuser.token
    except ExtendsUser.DoesNotExist:
        result = ExtendsUser.objects.create(user=user).token
    return result
