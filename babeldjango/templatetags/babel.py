# -*- coding: utf-8 -*-

from django.conf import settings
from django.template import Library
from django.utils.translation import to_locale, get_language
try:
    from pytz import timezone
except ImportError:
    timezone = None

from babeldjango.middleware import get_current_locale

babel = __import__('babel', {}, {}, ['core', 'support'])
Format = babel.support.Format
Locale = babel.core.Locale

register = Library()


def _get_format():
    locale = get_current_locale()
    if not locale:
        locale = Locale.parse(to_locale(get_language()))
    if timezone:
        tzinfo = timezone(settings.TIME_ZONE)
    else:
        tzinfo = None
    return Format(locale, tzinfo)


@register.filter
def datefmt(date=None, format='medium'):
    return _get_format().date(date, format=format)


@register.filter
def datetimefmt(datetime=None, format='medium'):
    return _get_format().datetime(datetime, format=format)


@register.filter
def timefmt(time=None, format='medium'):
    return _get_format().time(time, format=format)


@register.filter
def numberfmt(number):
    return _get_format().number(number)


@register.filter
def decimalfmt(number, format=None):
    return _get_format().decimal(number, format=format)


@register.filter
def currencyfmt(number, currency):
    return _get_format().currency(number, currency)


@register.filter
def percentfmt(number, format=None):
    return _get_format().percent(number, format=format)


@register.filter
def scientificfmt(number):
    return _get_format().scientific(number)
