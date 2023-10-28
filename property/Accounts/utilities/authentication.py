from django.db.models import Q
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
import jwt

from Accounts.models import User

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
    
def custom_authenticate(username=None, password=None):
    if '@' in username:
        kwargs = {'email': username}
    else:
        kwargs = {'username': username}
    try:
        my_user = User.objects.get(Q(**kwargs)&~Q(is_active=2))
    except User.DoesNotExist:
        return None
    else:
        if my_user.check_password(password):
            return my_user
    return my_user