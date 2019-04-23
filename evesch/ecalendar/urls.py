from django.conf.urls import url
from evesch.ecalendar import views

urlpatterns = [
    url(r'^$',
        views.calendar_default_view, {}, ),                       
    url(r'^monthly/$',
        views.calendar_monthly_view,
        {'template_name': 'ecalendar/calendar_monthly_view.html'},
        name='ecalendar_calendar_monthly_view'),
    url(r'^daily/$',
        views.calendar_daily_view,
        {'template_name': 'ecalendar/calendar_daily_view.html'},
        name='ecalendar_calendar_daily_view'),
]
