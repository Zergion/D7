from django import template
from datetime import datetime


register = template.Library()


@register.simple_tag()  # опишем наш тег вывода текущего времени
def current_time(format_string='%b/%d/%Y'):
    return datetime.utcnow().strftime(format_string)


@register.filter()
def currency(value):
   """
   value: значение, к которому нужно применить фильтр
   """

   return f'{value} Р'


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()