import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework import authentication, exceptions

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix != self.authentication_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        if cache.get(token) == "blacklisted":
            msg = "Token has been expired. Sign in again"
            raise exceptions.AuthenticationFailed(
                {"error": "status.401", "message": msg}
            )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            msg = "Authentication error. Unable to decode token"
            raise exceptions.AuthenticationFailed(
                {"error": "status.401", "message": msg}
            )
        try:
            user = User.objects.get(pk=payload["id"])
        except User.DoesNotExist:
            msg = "A user corresponding to this token was not found."
            raise exceptions.AuthenticationFailed(
                {"error": "status.401", "message": msg}
            )

        if not user.is_active:
            msg = "User in blocklist now"
            raise exceptions.AuthenticationFailed(
                {"error": "status.401", "message": msg}
            )
        return (user, token)
