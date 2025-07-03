from django import template
register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[int(position)]
    except (IndexError, ValueError, TypeError):
        return ""

@register.filter
def split(value, delimiter=","):
    return value.split(delimiter)