from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from accounts.api.base.serializers import BaseUserSerializer, BaseGoogleLoginSerializer
from accounts.models import User
from core.utils import get_logger, get_debug_str

logger = get_logger()


class AbstractBaseLoginView(GenericAPIView):
    authentication_classes = []

    class Meta:
        abstract = True

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(get_debug_str(request, request.user, serializer.errors))
            raise ValidationError(serializer.errors)

        user = serializer.validated_data.get('user')
        created = serializer.validated_data.get('created')
        device_id = serializer.validated_data.get('device_id')
        firebase_push_token = serializer.validated_data.get('firebase_push_token')

        user_serializer = BaseUserSerializer(instance=user, context={'request': request})
        token, _ = Token.objects.get_or_create(user=user)

        # if firebase_push_token is not None and firebase_push_token != '':
        #     try:
        #         FirebaseToken.objects.update_or_create(push_token=firebase_push_token, defaults={
        #             'user_id': user.id,
        #             'device_id': device_id.device_id
        #         })
        #     except Exception as e:
        #         logger.info(f"Push token update error --> {e}")

        resp = {
            'token': token.key,
            'token_type': 'token',
            'created': created,
            # 'user_info': user_serializer.data
        }
        return Response(resp, status=status.HTTP_200_OK)


class BaseGoogleLoginView(AbstractBaseLoginView):
    serializer_class = BaseGoogleLoginSerializer
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class BaseUserRetrieveAPIView(RetrieveAPIView):
    serializer_class = BaseUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
