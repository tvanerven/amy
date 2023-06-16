# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

DOMAINS = [
    "Performing Arts",
    "Visual Arts",
    "History",
    "Languages and Literature",
    "Law",
    "Philosophy",
    "Theology",
    "Anthropology",
    "Economics",
    "Geography",
    "Political Science",
    "Psychology",
    "Sociology",
    "Social Work",
    "Biology",
    "Chemistry",
    "Earth Science",
    "Space Sciences",
    "Physics",
    "Computer Science",
    "Mathematics",
    "Business",
    "Engineering and Technology",
    "Medicine and Health",
]


def add_knowledge_domains(apps, schema_editor):
    '''Add instances of KnowledgeDomains.'''
    KnowledgeDomain = apps.get_model('workshops', 'KnowledgeDomain')
    for domain in DOMAINS:
        KnowledgeDomain.objects.create(name=domain)


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0020_person_domains'),
    ]

    operations = [
        migrations.RunPython(add_knowledge_domains),
    ]
