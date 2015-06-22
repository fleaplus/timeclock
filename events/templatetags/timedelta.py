from django import template
from django.utils.timesince import timesince
from datetime import timedelta

register = template.Library()

@register.filter
def in_hours(value, arg=None):
    if type(value) is not timedelta:
        return value

    return value.total_seconds() / 60 / 60
