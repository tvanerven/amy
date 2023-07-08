#!/usr/bin/env python3
from django.core.management.base import BaseCommand

from workshops.models import Tag

TAGS = [
    {
        'name': 'automated-email' ,
        'priority': 0,
        'details': 'Only for automated emails',
    },
    {
        'name': 'Circuits',
        'priority': 4,
        'details': 'Events with only partial curriculum.',
    },
    {
        'name': 'online',
        'priority': 7,
        'details': 'Events taking place entirely online.',
    },
    {
        'name': 'ITT',
        'priority': 8,
        'details': 'Instructor Trainer Training (Trainer Training)',
    },
    {
        'name': 'cancelled',
        'priority': 9,
        'details': 'Events that were supposed to happen but due to some circumstances got cancelled',
    },
    {
        'name': 'unresponsive',
        'priority': 10,
        'details': "Events whose hosts and/or organizers aren't going to send data",
    },
    {
        'name': 'stalled',
        'priority': 11,
        'details': "Events with lost contact with the host or TTT events that aren't running.",
    },
    {
        'name': 'LSO',
        'priority': 13,
        'details': 'Lesson specific onboarding',
    },
    {
        'name': 'hackathon',
        'priority': 15,
        'details': 'Event is a hackathon',
    },
    {
        'name': 'CW',
        'priority': 16,
        'details': 'Curriculum Workshop',
    },
    {
        'name': 'TTT' ,
        'priority': 70,
        'details': 'Train the Trainers',
    },
    {
        'name': 'Pilot',
        'priority': 90,
        'details': 'To use for pilots of new or revamped curricula',
    },
    {
        'name': 'for-profit',
        'priority': 100,
            'details': 'Corporate or for-profit institutions that may be paying higher fees',
    },
    {
        'name': 'AE',
        'priority': 110,
        'details': 'Alumnus event',
    },
    {
        'name': 'HIC',
        'priority': 120,
        'details': 'Event occurring in a High income country',
    },
    {
        'name': 'LMIC',
        'priority': 130,
        'details': 'Event occurring in a Low or Middle Income Country',
    },
]


class Command(BaseCommand):

    help = "Setup tags according to what's desired"

    def handle(self, *args, **options):
        sords_tags_names = [sords_tag['name'] for sords_tag in TAGS]
        for tag in Tag.objects.all():
            if tag.name not in sords_tags_names:
                tag.delete()
            if tag.name in sords_tags_names:
                for entry in TAGS:
                    if entry['name'] == tag.name:
                        correct_tag = entry
                        tag.priority = correct_tag['priority']
                        tag.details = correct_tag['details']
                        tag.save()
        for tag_object in TAGS:
            obj, created = Tag.objects.get_or_create(**tag_object)
            if created:
                print(f"Created {obj.name}")
            if not created:
                print(f"{obj.name} already created, skipping.")
