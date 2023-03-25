from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    facebook_friends = models.ManyToManyField(to='User', verbose_name=_('Facebook friends'))

    def __str__(self):
        return self.username

    def get_full_name(self):
        return super().get_full_name()

    def get_facebook_picture(self):
        return self.get_social_profile_data(provider='facebook').get('picture', {}).get('data', {}).get('url', '')

    def get_social_account(self, provider='facebook'):
        return SocialAccount.objects.filter(user=self,
                                            provider=provider).first()

    def get_social_profile_data(self, provider='facebook'):
        social_account = self.get_social_account(provider=provider)
        try:
            return social_account.extra_data
        except (AttributeError, Exception):
            return {}
