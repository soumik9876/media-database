from urllib.error import HTTPError

from allauth.account import app_settings as allauth_settings
from allauth.account.signals import user_logged_in
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers

from accounts.api.base.serializers import BaseGoogleLoginSerializer, BaseUserSerializer
from accounts.models import User


# from billing.api.v1.serializers import  BillingProfileSerializer


class GoogleLoginSerializer(BaseGoogleLoginSerializer):
    pass


# noinspection PyMethodMayBeStatic
class UserSerializer(BaseUserSerializer):
    pass
