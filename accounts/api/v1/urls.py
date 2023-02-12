from django.urls import path

from accounts.api.v1.views import GoogleLoginView, UserRetrieveAPIView

appname = 'accounts-api-v1'
urlpatterns = [
    path('login/google/', GoogleLoginView.as_view(), name="google-login"),
    path('users/info/', UserRetrieveAPIView.as_view(), name="user-info"),
]
