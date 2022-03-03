import json
from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from io import StringIO, BytesIO
from requests import request
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.utils.creates_token_on_login import generate_access_token


def proceed_to_login(request, email, first_name, last_name):

    users = get_user_model().objects.filter(email=email).exists()

    if users == True:
        user = get_user_model().objects.get(email=email)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        return user
    else:
        user = get_user_model().objects.create_user(
            email=email, password=settings.SECRET_KEY
        )
        user = get_user_model().objects.get(email=email)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        return user
