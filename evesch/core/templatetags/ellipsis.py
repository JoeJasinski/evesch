from django import template  
register = template.Library()  


@register.filter("ellipsis")
def ellipsis(value, max_length):
    max_length = int(max_length)
    if len(value) > max_length:
        truncd_val = value[:max_length]
        #if value[max_length+1] != " ":
        #    truncd_val = truncd_val[:truncd_val.rfind(" ")]
        return  truncd_val + "..."
    return value