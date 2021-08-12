# Custom template filters

from django import template

register = template.Library()

@register.filter
def str_repr(obj):
    '''
    Get str representation of object
    '''
    return str(obj)

@register.filter
def skip_n_chars(coll, n):
    '''
    Skip n chars for each str in coll
    '''
    return list(map(lambda x: x[n:], coll))

@register.filter
def is_empty(coll):
    '''
    Is the collection empty?
    '''
    return len(coll) <= 0