from django.conf.urls.defaults import *
from ecalendar.views import *

urlpatterns = patterns('',
    url('^$', 'ecalendar.views.calendar_default_view', {}, ),                       
    url('^monthly/$', 'ecalendar.views.calendar_monthly_view', {'template_name':'ecalendar/calendar_monthly_view.html'}, name='ecalendar_calendar_monthly_view'),  
    url('^daily/$', 'ecalendar.views.calendar_daily_view', {'template_name':'ecalendar/calendar_daily_view.html'}, name='ecalendar_calendar_daily_view'),  
)
