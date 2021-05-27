# Generated by Django 2.2.18 on 2021-05-19 07:39

from django.db import migrations, models
import django.db.models.deletion


def select_membership_for_events(apps, schema_editor):
    """
    Set existing membership to event based on some criteria:
    * https://github.com/carpentries/amy/issues/1941
    """
    Event = apps.get_model("workshops", "Event")

    events = Event.objects.select_related("sponsor")

    for event in events:
        start = event.start

        # If event start is unknown, inform the user.
        if not start:
            print(
                f"Event {event} cannot be matched to membership: start date is unknown."
            )
            continue

        # If sponsor is unknown, inform the user.
        if not event.sponsor:
            print(
                f"Event {event} cannot be matched to membership: sponsor is unknown."
            )
            continue

        # Find memberships for selected sponsor where event start lies.
        memberships = event.sponsor.memberships.filter(
            agreement_start__lte=start, agreement_end__gte=start
        )

        # In case there are multiple memberships matching this criterium, find one
        # that expires the soonest.
        if len(memberships) > 1:
            membership = memberships.order_by("agreement_end").first()
        else:
            membership = memberships[0]

        event.membership = membership


class Migration(migrations.Migration):

    dependencies = [
        ("workshops", "0246_person_archived_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="membership",
            field=models.ForeignKey(
                blank=True,
                help_text="A membership this event should be counted towards.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="workshops.Membership",
            ),
        ),
        migrations.RunPython(select_membership_for_events, migrations.RunPython.noop),
    ]
