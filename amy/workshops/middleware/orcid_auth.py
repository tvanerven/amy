from django.conf import settings
from github import Github
from github.GithubException import UnknownObjectException
from social_core.exceptions import SocialAuthBaseException

from workshops.fields import GHUSERNAME_MAX_LENGTH_VALIDATOR, GHUSERNAME_REGEX_VALIDATOR


class NoPersonAssociatedWithOrcidAccount(SocialAuthBaseException):
    pass


def abort_if_no_user_found(user=None, **kwargs):
    """Part of Python-Social pipeline; aborts the authentication if no user
    can be associated with the specified GitHub username."""
    if user is None:
        raise NoPersonAssociatedWithOrcidAccount
