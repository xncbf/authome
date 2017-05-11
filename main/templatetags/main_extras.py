from django import template
from ..models import ExtendsUser
register = template.Library()


@register.filter
def get_or_create_token(value, user):
    if not value:
        value = ExtendsUser.objects.create(user=user)
    return value
