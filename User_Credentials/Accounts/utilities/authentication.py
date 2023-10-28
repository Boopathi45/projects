from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

from credentials_app.models import User

class SafeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        
        try:        
            if "Bearer" in authorization_header.split(" ")[0]:
                access_token = authorization_header.split(" ")[1]
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms='HS256')
            else:
                raise AuthenticationFailed("Invalid token prefix")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Access token expired")
        except IndexError:
            raise AuthenticationFailed("Token prefix missing")
        except Exception as e:
            raise AuthenticationFailed(str(e))        
        user = User.objects.filter(id=payload['id'], is_active=1).first()
        if user is None:
            raise AuthenticationFailed("User not found")

        return (user, None)