"""Archive_managment URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView
from dj_rest_auth.registration.views import VerifyEmailView
from users import views

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    # Rest Endpoint for password reset confirmation Email Sending
    re_path(
        r"^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,50})/$",
        TemplateView.as_view(),
        name="password_reset_confirm",
    ),
    # Custom Signup
    path("accounts/signup/", views.SignupView.as_view(), name="signup"),
    # Login
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    # Custom User Email Verification
    # Logout
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "account/email/verification/",
        views.VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    # This url with empty TemplateView is defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email content.
    # TODO: I commented this and created the same link below
    # so that the user can activate the account on click
    re_path(
        r"^accounts-confirm-email/(?P<key>[-:\w]+)/$",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
    # This url with empty TemplateView is defined just to allow reverse() call inside app, for example when email
    # account email verification is sent
    path(
        "accounts/confirm-email/",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    # Custom User Password Reset
    path(
        "accounts/password/reset/",
        views.PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    # Custom User Password Change
    path(
        "accounts/password/change/",
        views.PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    # Custom User Password Reset Confirm
    path(
        "accounts/password/reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
]