from evesch.org.models import Organization

def org_required(function=None, message=None):

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            message = kwargs.pop("message", None)
            org_short_name = kwargs.pop("org_short_name", None)
            if not message:
                current_org, message = Organization.objects.get_current_org(org_short_name)
            return view_func(request, message=message, current_org=current_org, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)
