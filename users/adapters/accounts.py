from __future__ import unicode_literals
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlsplit
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.
        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        site = get_current_site(request)
        location = reverse("account_confirm_email", args=[emailconfirmation.key])
        if len(settings.ALLOWED_HOSTS) == 0:
            proto = "https"
        else:
            proto = "http"

        bits = urlsplit(location)
        if not (bits.scheme and bits.netloc):
            uri = "{proto}://{domain}{url}".format(
                proto=proto, domain=site.domain, url=location,
            )
        else:
            uri = location
        return uri

    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        user = email_address.user
        user.is_active = True
        user.save()
        email_address.verified = True
        email_address.set_as_primary(conditional=True)
        email_address.save()

    def send_mail(self, template_prefix, email, context):
        site = get_current_site(self.request)
        if len(settings.ALLOWED_HOSTS) == 0:
            proto = "https"
        else:
            proto = "http"

        uri = "{proto}://{domain}".format(proto=proto, domain=site.domain,)
        if "password_reset_url" in context:
            action_uri = context["password_reset_url"]
            location = action_uri.split("accounts")[0]
            action_uri_ = action_uri.replace(location, uri + "/")
            context["password_reset_url"] = action_uri_
            msg = self.render_mail(template_prefix, email, context)
            msg.send()
        else:
            msg = self.render_mail(template_prefix, email, context)
            msg.send()
