from django.conf.urls import url
from evesch.report import views

urlpatterns = [
    url(r'^$',
        views.org_reports,
        {'template_name': 'report/org_report.html'},
        name='report_org_reports'),
    url(r'^by_user/$',
        views.org_reports,
        {'template_name': 'report/org_report.html', 'type': 'user'},
        name='report_org_reports_by_user'), 
    url(r'^by_eventtype/$',
        views.org_reports,
        {'template_name': 'report/org_report.html', 'type': 'eventtype'},
        name='report_org_reports_by_eventtype'),
    url(r'^by_event/$',
        views.org_reports,
        {'template_name': 'report/org_report.html', 'type': 'event'},
        name='report_org_reports_by_event'),
]
