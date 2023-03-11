from accounts.api.base.views import BaseGoogleLoginView, BaseUserRetrieveAPIView, BaseFacebookLoginAPIView
from accounts.api.v1.serializers import GoogleLoginSerializer, UserSerializer
from core.utils import get_logger

logger = get_logger()


class GoogleLoginView(BaseGoogleLoginView):
    serializer_class = GoogleLoginSerializer


class UserRetrieveAPIView(BaseUserRetrieveAPIView):
    serializer_class = UserSerializer


class FacebookLoginAPIView(BaseFacebookLoginAPIView):
    pass