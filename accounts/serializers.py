from django.conf import settings
from rest_framework import serializers
from library.sociallib import github
from library.register.register import register_social_user
from rest_framework.exceptions import *


class GithubSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = github.Github.validate(auth_token)

        try:
            email = user_data["email"]
            provider = "github"
        except:
            raise serializers.ValidationError(
                "The token  is invalid or expired. Please login again."
            )
        return register_social_user(
            provider=provider, user_id=None, email=email, name=None
        )
