from django import template
from urllib.parse import unquote

register = template.Library()


@register.filter
def file_name(url):
    return unquote(url.split('/')[-1]).lower().capitalize()
