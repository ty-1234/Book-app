# Ensure this file is named correctly and located in the templatetags directory within your app.
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        # Ensuring both values are converted to integers for multiplication
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''
