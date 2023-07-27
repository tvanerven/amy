#!/usr/bin/env python3
from django.core.management.base import BaseCommand

from workshops.models import Curriculum

CURRICULI = [
    {
        'carpentry': 'SWC',
        'slug': 'swc-cli',
        'name': 'Software Carpentry - Command line',
    },
    {
        'carpentry': 'SWC',
        'slug': 'swc-git',
        'name': 'Software Carpentry - Git',
    },
    {
        'carpentry': 'SWC',
        'slug': 'swc-r',
        'name': 'Software Carpentry - R',
    },
    {
        'carpentry': 'DC',
        'slug': 'dc-visualisation',
        'name': 'Visualisation',
    },
    {
        'carpentry': 'DC',
        'slug': 'dc-oarr',
        'name': 'Open and Responsible Research',
    },
    {
        'carpentry': 'DC',
        'slug': 'dc-rdm',
        'name': 'Research Data Management',
    },
    {
        'carpentry': '',
        'slug': 'c-infra',
        'name': 'Computational Infrastructure',
    },
    {
        'carpentry': 'DC',
        'slug': 'infosec',
        'name': 'Information Security',
    },
    {
        'carpentry': 'DC',
        'slug': 'dc-ac',
        'name': '',
    },
    {
        'carpentry': 'SWC',
        'slug': 'swc-ml',
        'name': 'Machine Learning',
    },
    {
        'carpentry': 'SWC',
        'slug': 'swc-nn',
        'name': 'Neural Networks',
    },
    {
        'carpentry': 'DC',
        'slug': 'dc-ds',
        'name': 'Data Stewardship',
    },
]


class Command(BaseCommand):

    help = "Setup curriculum according to what's desired"

    def handle(self, *args, **options):
        sords_curriculi_names = [sords_tag['name'] for sords_tag in CURRICULI]
        for curriculum in Curriculum.objects.all():
            if curriculum.name not in sords_curriculi_names:
                curriculum.delete()
            if curriculum.name in sords_curriculi_names:
                for entry in CURRICULI:
                    if entry['name'] == curriculum.name:
                        correct_tag = entry
                        curriculum.slug = correct_tag['slug']
                        curriculum.carpentry = correct_tag['carpentry']
                        curriculum.save()
        for curriculum_object in CURRICULI:
            obj, created = Curriculum.objects.get_or_create(**curriculum_object)
            if created:
                print(f"Created {obj.name}")
            if not created:
                print(f"{obj.name} already created, skipping.")
