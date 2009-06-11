from django import template  
register = template.Library()  

@register.filter('dict_lookup')
def dict_lookup(dict, key):
    return dict[key]