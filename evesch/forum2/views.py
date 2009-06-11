# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext

def forum_list(request, org_short_name, template_name=None):
    context = {}
    return render_to_response(template_name,context, context_instance=RequestContext(request))
    