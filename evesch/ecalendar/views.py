import calendar
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from evesch.org.models import Organization
from evesch.event.models import Event

calendar.setfirstweekday(6)


class MonthDay(object):
    date = 0
    events = []
    def __init__(self):
        pass

    def __str__(self):
        return "%s" % (self.date)


def calendar_monthly_view(request, template_name, org_short_name):

    current_org, message = Organization.objects.get_current_org(org_short_name)
    if message:
        template_name = "core/message.html"
        context = {'message':message,}
        return render(request, template_name, context)

    date_validate_error = False
    if "month" in request.GET and 'year' in request.GET:
        try:
            month = int(request.GET['month'])
            year = int(request.GET['year'])
            if month > 12 or month < 1:
                date_validate_error = True
            if year > 2100 or year < 1900:
                date_validate_error = True
            month_cursor = datetime(year, month, 1)
        except:
            date_validate_error = True
        if date_validate_error:
            return HttpResponseRedirect(
                reverse(
                    'ecalendar_calendar_monthly_view',
                    kwargs={'org_short_name': current_org.org_short_name}))
    else:
        month_cursor = datetime.now()
        
    month_next = month_cursor.month + 1
    month_prev = month_cursor.month - 1
    year_next = month_cursor.year
    year_prev = month_cursor.year
    if month_next == 13:
        month_next = 1
        year_next = year_next + 1
    if month_cursor.month - 1 == 0:
        month_prev = 12
        year_prev = year_prev - 1
    events = current_org.get_events().filter(
        event_date__year=month_cursor.year,
        event_date__month=month_cursor.month)
    #events = Event.objects.filter(event_date__year = month_cursor.year, event_date__month = month_cursor.month)
    month_cal = calendar.monthcalendar(month_cursor.year, month_cursor.month)
    monthcal = []
    for week in month_cal:
        weeklist = []
        for day in week:
            monthday = MonthDay()
            monthday.date = day
            monthday.events = events.filter(event_date__day=day)
            weeklist.append(monthday)
        monthcal.append(weeklist)
    context = {'monthcal': monthcal, "current_org": current_org,
               'month': month_cursor,
               'month_prev': month_prev, 'month_next': month_next,
               'year_prev': year_prev, 'year_next': year_next}
    return render(request, template_name, context)


def calendar_daily_view(request, template_name, org_short_name):

    current_org, message = Organization.objects.get_current_org(org_short_name)
    if message:
        template_name = "core/message.html"
        context = {'message': message}
        return render(request, template_name, context)
            
    date_validate_error = False
    if request.GET.__contains__("month") and request.GET.__contains__("year") and request.GET.__contains__("day"): 
        try:
            month = int(request.GET['month'])
            year = int(request.GET['year'])
            day = int(request.GET['day'])
            if month > 12 or month < 1:
                date_validate_error = True
            if year > 2100 or year < 1900:
               date_validate_error = True
            if day < 0 or day > 31:
                date_validate_error = True
            day_cursor = datetime(year, month, day)
        except:
            date_validate_error = True
        if date_validate_error:
            return HttpResponseRedirect(
                reverse('ecalendar_calendar_daily_view',
                        kwargs={'org_short_name': current_org.org_short_name,}))
    else:
        day_cursor = datetime.now()

    date_prev = day_cursor + timedelta(days=-1)
    date_next = day_cursor + timedelta(days=1)

    day_prev = date_prev.day
    day_next = date_next.day
    month_prev = date_prev.month
    month_next = date_next.month
    year_prev = date_prev.year
    year_next = date_next.year

    if month_next == 13:
        month_next = 1
        year_next = year_next + 1
    if day_cursor.month - 1 == 0:
        month_prev = 12
        year_prev = year_prev - 1
    events = current_org.get_events().filter(
        event_date__year=day_cursor.year, 
        event_date__month=day_cursor.month, 
        event_date__day=day_cursor.day,).order_by('event_name')   

    context = {
        'events': events, "current_org": current_org, 'day': day_cursor,
        'month_prev': month_prev, 'month_next': month_next,
        'year_prev': year_prev, 'year_next': year_next,
        'day_prev': day_prev, 'day_next': day_next, }
    return render(request, template_name, context)


def calendar_default_view(request, org_short_name):
    current_org, message = Organization.objects.get_current_org(org_short_name)
    if not message:
        return HttpResponseRedirect(
            reverse(
                'ecalendar_calendar_monthly_view',
                kwargs={'org_short_name': current_org.org_short_name}))
    else:
        template_name = "core/message.html"
        context = {'message': message}
    return render(request, template_name, context)