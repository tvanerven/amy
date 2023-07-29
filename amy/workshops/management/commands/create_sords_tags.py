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
        'name': 'online',
        'priority': 7,
        'details': 'Events taking place entirely online.',
    },
    {
        'name': 'Instructor Training',
        'priority': 8,
        'details': 'Instructor Trainer',
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
        'name': 'HIC',
        'priority': 100,
        'details': 'Event being done in a High Income Country',
    },
    {
        'name': 'LMIC',
        'priority': 130,
        'details': 'Event occurring in a Low or Middle Income Country',
    },
    {
        'name': 'ECR',
        'priority': 140,
        'details': 'Event is a school for ECRs',
    },
    {
        'name': 'Data Steward',
        'priority': 110,
        'details': 'Event is a Data Steward training event',
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
