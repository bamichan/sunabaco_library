from django import template
from http import cookies

register = template.Library()

@register.simple_tag(takes_context=True)
def cookie(context, cookie_name):  # could feed in additional argument to use as default value
    request = context['request']
    result = request.COOKIES.get(cookie_name, '')  # I use blank as default value
    return result
