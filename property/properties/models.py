from django.db import models

from property import settings

class Catogory(models.Model):
    name = models.CharField(max_length=30)

class Property(models.Model):

    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_property", related_query_name="user_property")
    propname      = models.CharField(max_length=50)
    posting_type  = models.ForeignKey(Catogory, on_delete=models.SET_NULL, null=True)
    address       = models.CharField(max_length=200)
    description   = models.CharField(max_length=200)
    amount        = models.DecimalField(decimal_places=2, max_digits=10)
    created_by    = models.IntegerField(default=0)
    created_on    = models.DateTimeField(auto_now_add=True)
    modify_by     = models.IntegerField(default=0)
    modify_on     = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'properties'

class Wallet(models.Model):

    wallet_owner   = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet', related_query_name='wallet')
    wallet_code    = models.CharField(max_length=255, blank=True, null=True)
    wallet_amount  = models.DecimalField(max_digits=18, decimal_places=2)
    wallet_limit   = models.DecimalField(max_digits=18, decimal_places=2)
    wallet_status  = models.BooleanField(default=False)
    wallet_address = models.JSONField(blank=True, null=True)
    notify         = models.IntegerField(default=0)
    created_by     = models.IntegerField(default=0)
    created_on     = models.DateTimeField(auto_now_add=True)
    modify_by      = models.IntegerField(default=0)
    modify_on      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallet_properties'