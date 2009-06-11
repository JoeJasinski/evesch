from django.conf.urls.defaults import *
from euser.views import *

urlpatterns = patterns('',
     url('^$', 'report.views.org_reports', {'template_name':'report/org_report.html'}, name='report_org_reports'),  
     url('^by_user/$', 'report.views.org_reports', {'template_name':'report/org_report.html', 'type':'user'}, name='report_org_reports_by_user'), 
     url('^by_eventtype/$', 'report.views.org_reports', {'template_name':'report/org_report.html', 'type':'eventtype'}, name='report_org_reports_by_eventtype'), 
     url('^by_event/$', 'report.views.org_reports', {'template_name':'report/org_report.html', 'type':'event'}, name='report_org_reports_by_event'), 
)
