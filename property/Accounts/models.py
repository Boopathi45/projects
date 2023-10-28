from django.db import models
from django.contrib.auth.models import AbstractUser

from Accounts.utilities.manager import UserManager

class User(AbstractUser):

    SUPER_ADMIN = 1
    ADMIN = 2
    QC = 3
    EDITOR = 4
    CLIENT = 5

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (QC, 'QC'),
        (EDITOR, 'Editor'),
        (CLIENT, 'Client')
    ]

    email       = models.EmailField(max_length=255, unique=True)
    username    = models.CharField(max_length=30)
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    password    = models.CharField(max_length=255)
    role_id     = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    is_active   = models.IntegerField(default=0)
    is_admin    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    created_by  = models.IntegerField(default=0)
    updated_at  = models.DateTimeField(auto_now=True)
    updated_by  = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user_accounts'