from django import template
from django.template.defaultfilters import floatformat
register = template.Library()

@register.filter(name='tableformat')
def tableformat(entry):
    if entry is None:
        return '-'
    elif is_numerical(entry):
        return floatformat(entry, -2)
    else:
        return entry

def is_numerical(str):
    try:
        float(str)
        return True
    except (ValueError, TypeError):
        return False