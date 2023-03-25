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

from accounts.models import User


# from billing.api.v1.serializers import  BillingProfileSerializer


class BaseGoogleLoginSerializer(serializers.Serializer):
    auth_code = serializers.CharField(label=_('Authorization code'), required=False)
    access_token = serializers.CharField(label=_('Access Token'), required=False)
    firebase_push_token = serializers.CharField(label=_('Firebase Push Token'), required=False)

    def _get_request(self):
        request = self.context.get('request')
        if not isinstance(request, HttpRequest):
            request = request._request
        return request

    def get_social_login(self, adapter, app, token, response):
        request = self._get_request()
        social_login = adapter.complete_login(request, app, token, response=response)
        social_login.token = token
        return social_login

    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _("View is not defined, pass it as a context variable")
            )

        adapter_class = getattr(view, 'adapter_class', None)
        client_class = getattr(view, 'client_class', None)

        if not adapter_class:
            raise serializers.ValidationError(_("Define adapter_class in view"))

        if not client_class:
            raise serializers.ValidationError(_("Define client_class in view"))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)
        callback_url = adapter.get_callback_url(request, app)
        provider = adapter.get_provider()
        scope = provider.get_scope(request)

        auth_code = attrs.get('auth_code')
        access_token = attrs.get('access_token')

        if auth_code:
            client = client_class(
                request,
                app.client_id, app.secret,
                adapter.access_token_method,
                adapter.access_token_url,
                callback_url,
                scope,
                scope_delimiter=adapter.scope_delimiter,
                headers=adapter.headers,
                basic_auth=adapter.basic_auth
            )

            try:
                token = client.get_access_token(auth_code)
            except OAuth2Error as e:
                raise serializers.ValidationError({'auth_code': e})

            access_token = token['access_token']

        elif access_token:
            token = {'access_token': access_token}

        else:
            raise serializers.ValidationError({'auth_code': 'Auth Code or Access Token is required'})

        social_token = adapter.parse_token(token)
        social_token.app = app

        current_dt = timezone.now()

        try:
            login = self.get_social_login(adapter, app, social_token, access_token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_("Incorrect value"))

        if not login.is_existing:
            if getattr(allauth_settings, 'UNIQUE_EMAIL', False):
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _("User is already registered with this e-mail address.")
                    )

            login.lookup()
            login.save(request, connect=True)

        user = login.account.user
        created = user.date_joined >= current_dt
        attrs['user'], attrs['created'] = user, created
        user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# noinspection PyMethodMayBeStatic
class BaseUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(label=_('Name'))
    facebook_picture = serializers.SerializerMethodField(label=_('Photo URL'))
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'first_name', 'last_name', 'email', 'facebook_picture', 'is_superuser'
        ]

    def get_name(self, obj: User):
        social_profile = obj.get_social_profile_data()
        return social_profile.get('name')

    def get_facebook_picture(self, obj: User):
        return obj.get_facebook_picture()

    def update(self, instance, validated_data):
        return validated_data
