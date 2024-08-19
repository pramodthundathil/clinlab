from django import template
from itertools import groupby
from operator import attrgetter

register = template.Library()

@register.filter
def groupby(value, arg):
    sorter = attrgetter(arg)
    grouped = groupby(sorted(value, key=sorter), sorter)
    return [(key, list(group)) for key, group in grouped]