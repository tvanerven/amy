#!/usr/bin/env python3
#
import csv

from django.core.management.base import BaseCommand
from django_countries import countries as Countries

from workshops.models import Person

def clean_family_name(name):
    words = name.split(" ")
    result = ""
    for word in words:
        result.join(word.lower().capitalize())
    return result

def clean_affiliation(affiliation: str):
    if not affiliation:
        affiliation = "Unknown"
    return affiliation.replace(":", ",")

def is_email_present(person_dict):
    if person_dict.get('email'):
        return True
    return False

def dictify(row):
    return {
        'personal': row[0],
        'family': clean_family_name(row[1]),
        'country': row[2],
        'affiliation': clean_affiliation(row[4]) if row[3] else '',
        'occupation': row[4] if row[4] else '',
        'email': row[5],
        'username': row[5]
    }

def check_for_duplicate(person_dict):
    possible_match = Person.objects.filter(personal=person_dict['personal'], family=person_dict['family'])
    if possible_match.exists():
        print(f"Possible match detected: {possible_match} and {person_dict['personal']} could be the same")
        return True, possible_match
    return False, None

def attempt_to_create_person(row):
    person_dict = dictify(row)
    if is_email_present(person_dict):
        duplicated, match = check_for_duplicate(person_dict)
        print("Attempting to import: ", person_dict)
        if duplicated:
            match.update(**person_dict)
            print(f"{person_dict['personal']} has been updated!")
        else:
            Person.objects.create(**person_dict)
            print(f"{person_dict['personal']} has been created!")


class Command(BaseCommand):


    help = "Import users stored in import_data.csv file in same folder"

    def handle(self, *args, **options):
        with open('import_data.csv', newline='') as data:
            reader = csv.reader(data, delimiter=';', quotechar='"')
            for row in reader:
                attempt_to_create_person(row=row)
