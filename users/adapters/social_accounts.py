from __future__ import absolute_import
import uuid
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from allauth.account import app_settings as account_settings
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.app_settings import EmailVerificationMethod
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import (
    deserialize_instance,
    email_address_exists,
    import_attribute,
    serialize_instance,
    valid_email_or_none,
)
from allauth import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from users.models.user_auth import UserAuth
from users.models.profile import Profile
from users.models.actor import Actor


class KorioneSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, or linkedin but allauth takes care of this case so just
        # ignore it
        if (
            "email" not in sociallogin.account.extra_data
            and sociallogin.account.get_provider().name.lower() != "linkedin"
        ):
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            try:
                # Get email from Facebook, Twitter, and Google provider
                email = sociallogin.account.extra_data["email"].lower()
            except KeyError:
                # Get email from LinkedIn provider
                email = sociallogin.account.extra_data["elements"][0]["handle~"][
                    "emailAddress"
                ].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. In case of auto-signup,
        the signup form is not available.
        """
        u = sociallogin.user

        actor = Actor.objects.create(id=uuid.uuid4(), is_active=True)
        profile = Profile.objects.create(actor_id=actor, is_active=True)
        u.profile_id = profile
        u.is_validated = True
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            get_account_adapter().populate_username(request, u)
        sociallogin.save(request)

        # Make sur that the new user emailAddress is set to Verified=True
        # This case appears especially for Linkedin Provider
        EmailAddress.objects.filter(user=u).update(verified=True)
        return u

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        assert request.user.is_authenticated
        url = reverse("socialaccount_connections")
        return url

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.
        For convenience, we populate several common fields.
        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.
        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        name = data.get("name")
        user = sociallogin.user
        user_username(user, username or "")
        user_email(user, valid_email_or_none(email) or "")
        name_parts = (name or "").partition(" ")
        user_field(user, "first_name", first_name or name_parts[0])
        user_field(user, "last_name", last_name or name_parts[2])
        return user
