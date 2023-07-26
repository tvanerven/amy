from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from workshops.middleware.orcid_auth import NoPersonAssociatedWithOrcidAccount


class OrcidAuthMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, NoPersonAssociatedWithOrcidAccount):
            messages.error(
                request, "No account is associated with your OrcID account."
            )
            return redirect(reverse("login"))
