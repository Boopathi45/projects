from django.db import models
from django.contrib.auth.models import AbstractUser

from User_Credentials import settings
from credentials_app.utilities.manager import UserManager


class User(AbstractUser):
    email        = models.EmailField(max_length=255, unique=True)
    username     = models.CharField(max_length=30)
    first_name   = models.CharField(max_length=100)
    last_name    = models.CharField(max_length=100)
    password     = models.CharField(max_length=255)
    is_active    = models.IntegerField(default=0)
    is_admin     = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    created_by   = models.IntegerField(default=0)
    updated_at   = models.DateTimeField(auto_now=True)
    updated_by   = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user_accounts'


class Credentials(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credential', related_query_name='credential')
    title       = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    value       = models.CharField(max_length=2000)
    expire_on   = models.DateTimeField()
    share_info  = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'user_credential'


class BlacklistToken(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blacklist_token")
    token      = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blacklist_token'
