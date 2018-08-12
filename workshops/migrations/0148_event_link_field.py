# Generated by Django 2.1 on 2018-08-12 16:43

from django.db import migrations, models
from django.db.models import F
import django.db.models.deletion


def copy_old_eventrequest_relation(apps, schema_editor):
    """Basically the relation name was changed, but also the point of
    declaration, so the way this migration rewrites data is a little bit
    complicated. See comment below."""

    Event = apps.get_model('workshops', 'Event')
    EventRequest = apps.get_model('workshops', 'EventRequest')

    events = Event.objects.exclude(request=None).select_related('request')

    # we're going the other way around in this rewrite: instead of writing
    # `event.eventrequest = event.request`, we're finding a proper EventRequest
    # and assigning its `event` - because the former doesn't work
    for event in events:
        EventRequest.objects.filter(id=event.request_id).update(event=event.id)


def fill_eventsubmission_event_link(apps, schema_editor):
    """Find possible candidates for the link by using the declared submission
    URL."""
    Event = apps.get_model('workshops', 'Event')
    EventSubmission = apps.get_model('workshops', 'EventSubmission')

    for submission in EventSubmission.objects.filter(active=False):
        try:
            event = Event.objects.get(url=submission.url)
            submission.event = event
            submission.save()
        except Event.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0147_auto_20180802_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventrequest',
            name='event',
            field=models.OneToOneField(blank=True, help_text='Link to the event instance created or otherwise related to this object.', null=True, on_delete=django.db.models.deletion.PROTECT, to='workshops.Event', verbose_name='Linked event object'),
        ),
        migrations.AddField(
            model_name='dcselforganizedeventrequest',
            name='event',
            field=models.OneToOneField(blank=True, help_text='Link to the event instance created or otherwise related to this object.', null=True, on_delete=django.db.models.deletion.PROTECT, to='workshops.Event', verbose_name='Linked event object'),
        ),
        migrations.AddField(
            model_name='eventsubmission',
            name='event',
            field=models.OneToOneField(blank=True, help_text='Link to the event instance created or otherwise related to this object.', null=True, on_delete=django.db.models.deletion.PROTECT, to='workshops.Event', verbose_name='Linked event object'),
        ),
        migrations.AlterField(
            model_name='event',
            name='request',
            field=models.ForeignKey(blank=True, help_text='Backlink to the request that created this event.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_request_original', to='workshops.EventRequest'),
        ),
        migrations.RunPython(copy_old_eventrequest_relation),
        migrations.RunPython(fill_eventsubmission_event_link),
        migrations.RemoveField(
            model_name='event',
            name='request',
        ),
    ]
