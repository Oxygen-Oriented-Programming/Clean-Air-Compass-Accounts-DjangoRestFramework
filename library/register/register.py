from rest_framework.authtoken.models import Token

from accounts.models import User
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():
        new_user = User.objects.get(email=email)

        registered_user = User.objects.get(email=email)

        Token.objects.filter(user=registered_user).delete()
        Token.objects.create(user=registered_user)
        new_token = list(
            Token.objects.filter(user_id=registered_user).values("key")
        )

        return {
            "username": registered_user.username,
            "email": registered_user.email,
            "tokens": str(new_token[0]["key"]),
        }
    if provider == 'github':
            user = {"username": email, "email": email, "password": settings.GITHUB_SOCIAL_SECRET}
            user = User.objects.create_user(**user)
            user.is_active = True
            user.auth_provider = provider
            user.save()
            new_user = User.objects.get(email=email)
            new_user.check_password(settings.GITHUB_SOCIAL_SECRET)
            Token.objects.create(user=new_user)
            new_token = list(Token.objects.filter(user_id=new_user).values("key"))
            return {
                "email": new_user.email,
                "username": new_user.username,
                "tokens": str(new_token[0]["key"]),
            }
    if provider == 'google':
            print("newaccount")
            user = {"username": email, "email": email, "password": settings.GOOGLE_SOCIAL_SECRET}
            user = User.objects.create_user(**user)
            user.is_active = True
            user.auth_provider = provider
            user.save()
            new_user = User.objects.get(email=email)
            new_user.check_password(settings.GOOGLE_SOCIAL_SECRET)
            Token.objects.create(user=new_user)
            new_token = list(Token.objects.filter(user_id=new_user).values("key"))
            return {
                "email": new_user.email,
                "username": new_user.username,
                "tokens": str(new_token[0]["key"]),
            }
