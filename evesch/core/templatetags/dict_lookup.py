from django import template
register = template.Library()


@register.filter('dict_lookup')
def dict_lookup(dicti, key):
    return dicti[key]
