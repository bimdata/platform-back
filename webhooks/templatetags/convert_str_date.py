import datetime

from dateutil.parser import parse
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_str_date(value: str) -> datetime.datetime:
    return parse(value)


@register.filter
@stringfilter
def convert_isostr_date(value: str) -> datetime.datetime:
    date = datetime.date.fromisoformat(value)
    return datetime.datetime.combine(date, datetime.datetime.min.time())
