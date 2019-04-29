from django import template
from evesch.core.lib import text_vs_bg
register = template.Library()


@register.filter("color_correct")
def color_correct(bgcolor):
    return text_vs_bg(bgcolor)
