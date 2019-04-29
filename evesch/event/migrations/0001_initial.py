# Generated by Django 2.1.8 on 2019-04-22 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('org', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('att_added_date', models.DateTimeField(auto_now_add=True, db_column='att_added_date', verbose_name='Register Date')),
                ('att_ip', models.GenericIPAddressField(blank=True, db_column='att_ip', null=True, verbose_name='Attendee IP Address')),
                ('att_hours', models.FloatField(blank=True, db_column='att_hours', null=True, verbose_name='Attendee Hours')),
                ('att_col1', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 1')),
                ('att_col2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 2')),
                ('att_col3', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 3')),
                ('att_col4', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 4')),
                ('att_col5', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 5')),
                ('att_col6', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 6')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(db_index=True, max_length=64, verbose_name='Event Name')),
                ('event_hash', models.CharField(db_index=True, max_length=8, unique=True, verbose_name='Event Hash')),
                ('event_active', models.NullBooleanField(default=True, verbose_name='Does the Event Exist?')),
                ('event_open', models.BooleanField(default=True, verbose_name='Event open to Add Attendees')),
                ('event_signup_deadline', models.DateTimeField(blank=True, null=True, verbose_name='Date that you must register by.')),
                ('event_date', models.DateTimeField(db_index=True, verbose_name='Date and Time of Event')),
                ('event_created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Event Created Date')),
                ('event_desc', models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='Event Description')),
                ('event_max_attendees', models.IntegerField(blank=True, null=True, verbose_name='Maximum Number of Addendees')),
                ('event_priority', models.IntegerField(blank=True, null=True, verbose_name='Event Priority')),
                ('event_track_hours', models.BooleanField(default=False, verbose_name='Should we track the hours attendees spend at events?')),
                ('att_header_col1', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 1 Header')),
                ('att_require_col1', models.BooleanField(default=False, verbose_name='Required')),
                ('att_type_col1', models.IntegerField(choices=[(0, 'Textbox'), (1, 'Checkbox'), (2, 'Dropdown'), (3, 'Number')], default=0, verbose_name='Custom Field Type 1')),
                ('att_type_drop_col1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom Field Type 1 Dropdown')),
                ('att_header_col2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 2 Header')),
                ('att_require_col2', models.BooleanField(default=False, verbose_name='Required')),
                ('att_type_col2', models.IntegerField(choices=[(0, 'Textbox'), (1, 'Checkbox'), (2, 'Dropdown'), (3, 'Number')], default=0, verbose_name='Custom Field Type 2')),
                ('att_type_drop_col2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom Field Type 2 Dropdown')),
                ('att_header_col3', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 3 Header')),
                ('att_require_col3', models.BooleanField(default=False, verbose_name='Required')),
                ('att_type_col3', models.IntegerField(choices=[(0, 'Textbox'), (1, 'Checkbox'), (2, 'Dropdown'), (3, 'Number')], default=0, verbose_name='Custom Field Type 3')),
                ('att_type_drop_col3', models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom Field Type 3 Dropdown')),
                ('att_header_col4', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 4 Header')),
                ('att_require_col4', models.BooleanField(default=False, verbose_name='Required')),
                ('att_type_col4', models.IntegerField(choices=[(0, 'Textbox'), (1, 'Checkbox'), (2, 'Dropdown'), (3, 'Number')], default=0, verbose_name='Custom Field Type 4')),
                ('att_type_drop_col4', models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom Field Type 4 Dropdown')),
                ('att_header_col5', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 5 Header')),
                ('att_require_col5', models.BooleanField(default=False, verbose_name='Required')),
                ('att_type_col5', models.IntegerField(choices=[(0, 'Textbox'), (1, 'Checkbox'), (2, 'Dropdown'), (3, 'Number')], default=0, verbose_name='Custom Field Type 5')),
                ('att_type_drop_col5', models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom Field Type 5 Dropdown')),
                ('att_header_col6', models.CharField(blank=True, max_length=20, null=True, verbose_name='Column 6 Header')),
                ('att_require_col6', models.BooleanField(default=False, verbose_name='Required')),
                ('att_type_col6', models.IntegerField(choices=[(0, 'Textbox'), (1, 'Checkbox'), (2, 'Dropdown'), (3, 'Number')], default=0, verbose_name='Custom Field Type 6')),
                ('att_type_drop_col6', models.CharField(blank=True, max_length=255, null=True, verbose_name='Custom Field Type 6 Dropdown')),
                ('event_coordinators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Event Coordinators')),
                ('event_creator_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_creator', to=settings.AUTH_USER_MODEL, verbose_name='Event Creator')),
                ('event_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Organization', verbose_name='Organization Sponsoring the Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(db_column='type_name', max_length=32, verbose_name='Event Type')),
                ('type_hash', models.CharField(db_column='type_hash', db_index=True, max_length=8, unique=True, verbose_name='Event Type Hash')),
                ('type_desc', models.CharField(blank=True, db_column='type_desc', max_length=256, null=True, verbose_name='Event Type Description')),
                ('type_color', models.CharField(blank=True, max_length=15, null=True, verbose_name='Event Type Color')),
                ('type_track_hours', models.BooleanField(db_column='type_track_hours', default=False, verbose_name='Track Hours for events of this type?')),
                ('type_active', models.BooleanField(default=True, help_text='Has the event been disabled?', verbose_name='Event Type Enabled')),
                ('org_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.EventType', verbose_name='Type of Event'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='att_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Event', verbose_name='Event to Attend'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='att_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User Attending'),
        ),
    ]