from django.template import Library, Node
from django.template import TemplateSyntaxError
from evesch.org.models import Organization
#from django.db.models import get_model

register = Library()


class IsOrgMember(Node):
    def __init__(self, org, user):
        self.org = org
        self.user = user

    def render(self, context):
        cur_org, message = Organization.objects.get_current_org(self.org)
        if message:
            return False
        else:
            return True


def is_org_member(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError("is_org_member tag takes exactly 2 arguments")
    return IsOrgMember(bits[1], bits[2])


is_org_member = register.tag(is_org_member)
