from django import template

register = template.Library()

@register.filter(name='format_category')
def format_category(value):
    if not value:
        return "No Category"  # or however you wish to denote an empty category
    return ', '.join(value)
