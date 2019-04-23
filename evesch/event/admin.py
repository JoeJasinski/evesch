from django.contrib import admin
from evesch.event.models import EventType, Event, Attendee


class EventTypeAdmin(admin.ModelAdmin):
    list_display = [
        'type_name',
        'type_active',
        'type_hash',
        'type_desc',
        'type_color',
        'org_name']
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'event_name',
        'event_creator_name',
        'event_created_date',
        'event_date',
        'event_type',
        'event_priority']
    list_filter = [
        'event_name',
        'event_creator_name',
        'event_date']
class AttendeeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'att_name',
        'att_added_date',
        'att_ip']


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, AttendeeAdmin)
