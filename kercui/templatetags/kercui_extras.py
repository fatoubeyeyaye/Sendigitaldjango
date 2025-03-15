from django import template
import pprint
from pprint import pprint
from pprint import pformat

register = template.Library()

@register.filter
def pprint(value):
    return pformat(value)