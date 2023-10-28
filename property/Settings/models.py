from django.db import models

from Accounts.models import User

class MasterJobImageCount(models.Model):
    image_count        = models.IntegerField(unique=True)
    created_on         = models.DateTimeField(auto_now_add=True)
    created_by         = models.IntegerField(default=0)
    updated_on         = models.DateTimeField(auto_now=True)
    updated_by         = models.IntegerField(default=0)

    class Meta:
        db_table = 'master_job_image_count'

class MasterTurnAroundTime(models.Model):
    image_count_id     = models.ForeignKey(MasterJobImageCount, on_delete=models.CASCADE, db_column='image_count_id', related_name='job_duration', related_query_name='job_duration')
    duration           = models.IntegerField()
    price              = models.DecimalField(max_digits=18, decimal_places=2)
    is_active          = models.BooleanField(default=False)
    created_on         = models.DateTimeField(auto_now_add=True)
    created_by         = models.IntegerField(default=0)
    updated_on         = models.DateTimeField(auto_now=True)
    updated_by         = models.IntegerField(default=0)

    class Meta:
        db_table = 'master_turn_around_time'

class WorkSample(models.Model):
    title       = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    media_type  = models.CharField(max_length=100)
    media       = models.JSONField(blank=True, null=True)
    user_id     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id', related_query_name='user_id', db_column='user_id')
    created_on  = models.DateTimeField(auto_now_add=True)
    created_by  = models.IntegerField(default=0)
    updated_on  = models.DateTimeField(auto_now=True)
    updated_by  = models.IntegerField(default=0)

    class Meta:
        db_table = 'work_sample'