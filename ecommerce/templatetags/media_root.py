from  django import template
from django.conf import settings


register = template.Library()

@register.tag
def media_root():
    return settings.MEDIA_ROOT