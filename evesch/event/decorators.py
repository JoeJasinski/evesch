

def event_required(function=None, message=None):

    def _dec(view_func):
        def _view(request, *args, **kwargs):
            message = kwargs.pop("message", None)
            event_hash = kwargs.pop("event_hash", None)
            current_org = kwargs["current_org"]
            if not message:
                current_event, message = current_org.get_current_event(event_hash, message) 
            return view_func(request, message=message, current_event=current_event, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)
