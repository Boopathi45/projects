from django.db.models import Q

from credentials_app.models import User

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