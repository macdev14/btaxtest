from django import template

register = template.Library()

@register.simple_tag
def retorna_id(obj):
    return obj['_id']