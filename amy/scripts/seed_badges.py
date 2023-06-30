import logging
from typing import TypedDict

from workshops.models import Badge
from workshops.utils.seeding import deprecate_models, seed_models

logger = logging.getLogger("amy")

# If an entry needs to be removed from the database, remove it from e.g.
# `EMAIL_TEMPLATES`, and put its' ID in `DEPRECATED_EMAIL_TEMPLATES`.

DEPRECATED_BADGES: list[str] = []

BadgeDef = TypedDict(
    "BadgeDef",
    {
        "name": str,
        "title": str,
        "criteria": str,
    },
)

BADGES: list[BadgeDef] = [
    {
        "name": "maintainer",
        "title": "Maintainer",
        "criteria": "Maintainer of Software or Data Carpentry lesson",
    },
    {
        "name": "trainer",
        "title": "Instructor Trainer",
        "criteria": "Teaching instructor training workshops",
    },
    {
        "name": "creator",
        "title": "Creator",
        "criteria": "Creating learning materials and other content",
    },
    {
        "name": "organizer",
        "title": "Organizer",
        "criteria": "Organizing workshops and learning groups",
    },
    {
        "name": "instructor",
        "title": "Instructor",
        "criteria": "Teaching at The Carpentries workshops or online",
    },
    {
        "name": "tester",
        "title": "Tester",
        "criteria": "Teaching at The Carpentries workshops or online",
    },
    {
        "name": "alumnus",
        "title": "Alumnus",
        "criteria": "Alumnus",
    },
    {
        "name": "co-chair",
        "title": "Co-Chair",
        "criteria": "Is co-chair",
    },
    {
        "name": "ab-member",
        "title": "AB Member",
        "criteria": "Is member of AB",
    },
    {
        "name": "funder",
        "title": "Funder",
        "criteria": "Provides funding",
    },
    {
        "name": "ab-chair",
        "title": "AB Chair",
        "criteria": "Is chair of AB",
    },
    {
        "name": "helper",
        "title": "Helper",
        "criteria": "Is a helper",
    },
    {
        "name": "instructor-trainee",
        "title": "Instructor Trainee",
        "criteria": "Is an instructor trainee",
    },
    {
        "name": "support",
        "title": "Support",
        "criteria": "Tasked with support work",
    },
    {
        "name": "learner",
        "title": "Learner",
        "criteria": "Intends to learn or is enrolled in a training programme",
    },
    {
        "name": "host",
        "title": "Host",
        "criteria": "Acts as host for training programmes",
    },
    {
        "name": "reviewer",
        "title": "Reviewer",
        "criteria": "Reviews training materials",
    },
]

# --------------------------------------------------------------------------------------


def badge_transform(badge_def: dict) -> Badge:
    return Badge(**badge_def)


def run() -> None:
    names = [item['name'] for item in BADGES]
    Badge.objects.all().exclude(name__in=names).delete()
    seed_models(Badge, BADGES, "name", badge_transform, logger)

    deprecate_models(Badge, DEPRECATED_BADGES, "name", logger)
