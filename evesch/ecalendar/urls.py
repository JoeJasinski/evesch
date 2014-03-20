from django.conf.urls import patterns, include, url
from evesch.ecalendar.views import *

urlpatterns = patterns('',
    url('^$', 'evesch.ecalendar.views.calendar_default_view', {}, ),                       
    url('^monthly/$', 'evesch.ecalendar.views.calendar_monthly_view', {'template_name':'ecalendar/calendar_monthly_view.html'}, name='ecalendar_calendar_monthly_view'),  
    url('^daily/$', 'evesch.ecalendar.views.calendar_daily_view', {'template_name':'ecalendar/calendar_daily_view.html'}, name='ecalendar_calendar_daily_view'),  
)
