from django import template

register = template.Library()

@register.filter
def sort_by_name(users):
    return sorted(users, key=lambda u: (u.first_name, u.last_name))

@register.filter
def split_by(value, delimiter=','):
    """Splits a string by the given delimiter, handling None values."""
    if value:
        return value.split(delimiter)
    return []  # Return an empty list if value is None