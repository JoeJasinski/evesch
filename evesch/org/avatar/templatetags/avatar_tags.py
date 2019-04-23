import urllib

from django import template
from django.utils.translation import ugettext as _

from evesch.org.avatar import AVATAR_DEFAULT_URL

from evesch.org.models import Organization

register = template.Library()

def avatar_url(org, size=300):
    avatars = org.avatar_set.order_by('-date_uploaded')
    primary = avatars.filter(primary=True)
    if primary.count() > 0:
        avatar = primary[0]
    elif avatars.count() > 0:
        avatar = avatars[0]
    else:
        avatar = None
    if avatar is not None:
        if not avatar.thumbnail_exists(size):
            avatar.create_thumbnail(size)
        return avatar.avatar_url(size)
    else:
        return AVATAR_DEFAULT_URL
register.simple_tag(avatar_url)

def avatar(org_short_name, size=300):

    try:
        org = Organization.objects.get(org_short_name=org_short_name)
        alt = str(org.org_name)
        url = avatar_url(org, size)
    except Organization.DoesNotExist:
        url = AVATAR_DEFAULT_URL
        alt = _("Default Avatar")

    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (url, alt, size, ((size * 3) / 4))
register.simple_tag(avatar)

def render_avatar(avatar, size=80):
    if not avatar.thumbnail_exists(size):
        avatar.create_thumbnail(size)
    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (
        avatar.avatar_url(size), str(avatar), size, ((size * 3) / 4))
register.simple_tag(render_avatar)


def any_avatar_url(avatar, size=300):
    try: 
        return avatar.avatar_url(size)
    except:
        return AVATAR_DEFAULT_URL
register.simple_tag(any_avatar_url)