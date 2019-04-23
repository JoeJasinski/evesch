# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import RequestContext


def forum_list(request, org_short_name, template_name=None):
    context = {}
    return render(request, template_name, context)
    