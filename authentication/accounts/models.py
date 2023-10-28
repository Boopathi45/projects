from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from helper.manager import UserManager

class User(AbstractBaseUser):

    email         = models.EmailField(max_length=255, unique=True)
    username      = models.CharField(max_length=30)
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    password      = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10, blank=True)
    is_active     = models.IntegerField(default=0)
    is_admin      = models.BooleanField(default=False)
    headshot      = models.JSONField(blank=True, null=True)
    last_login    = models.DateTimeField(null=True, blank=True)
    created_on    = models.DateTimeField(auto_now_add=True)
    created_by    = models.IntegerField(default=0)
    updated_on    = models.DateTimeField(auto_now=True)
    updated_by    = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user_accounts'

class UserTokenVerify(models.Model):

    email               = models.EmailField(max_length=255)
    phone_number        = models.CharField(max_length=255, blank=True, null=True)
    verification_code   = models.CharField(max_length=255)
    code_generated_on   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_token'