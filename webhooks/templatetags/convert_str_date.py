import datetime

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_str_date(value: str) -> datetime.datetime:
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")


@register.filter
@stringfilter
def convert_isostr_date(value: str) -> datetime.datetime:
    date = datetime.date.fromisoformat(value)
    return datetime.datetime.combine(date, datetime.datetime.min.time())
