from django import template  
register = template.Library()


@register.filter(name='org_permissions')
def org_permissions(user, obj):
    return obj.org_perms(user)


@register.filter(name='event_permissions')
def event_permissions(user, obj):
    return obj.event_perms(user)

