from django.db import models

from Accounts.models import User

class JobStatus(models.Model):

    status_id   = models.IntegerField(unique=True)
    status_name = models.CharField(max_length=100)
    is_active   = models.BooleanField(default=True)

    class Meta:
        db_table = 'job_status'

class Job(models.Model):

    job_id           = models.CharField(max_length=250, unique=True)
    title            = models.CharField(max_length=250, blank=True, null=True)
    turn_around_time = models.IntegerField(blank=True, null=True)
    media            = models.JSONField(blank=True, null=True)
    storage_consumed = models.JSONField(blank=True, null=True)
    services_lst     = models.JSONField(blank=True, null=True)
    preferences_lst  = models.JSONField(blank=True, null=True)
    gross_price      = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    net_price        = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    user_id          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_job', db_column='user_job', related_query_name='user_job')
    status           = models.ForeignKey(JobStatus, on_delete=models.SET_NULL, null=True, related_name='job_status', db_column='job_status', related_query_name='job_status')
    created_by       = models.IntegerField(default=0)
    created_on       = models.DateTimeField(auto_now_add=True)
    updated_by       = models.IntegerField(default=0)
    updated_on       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jobs'

class JobPayment(models.Model):

    item_list       = models.JSONField()
    coupon_code     = models.CharField(max_length=100, blank=True, null=True)
    gross_price     = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    net_price       = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, blank=True, null=True)
    discount_type   = models.BooleanField(default=False)
    job_id          = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='job_payment', related_query_name='job_payment', db_column='job_payment')
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment', related_query_name='user_payment', db_column='user_payment')
    created_by      = models.IntegerField(default=0)
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_by      = models.IntegerField(default=0)
    updated_on      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'JobPayment'