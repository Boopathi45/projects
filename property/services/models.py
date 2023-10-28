from django.db import models

class Services(models.Model):

    name         = models.CharField(max_length=20)
    description  = models.CharField(max_length=250, blank=True, null=True)
    price        = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    file_type    = models.CharField(max_length=50)
    before_image = models.JSONField(blank=True, null=True)
    after_image  = models.JSONField(blank=True, null=True)
    created_by   = models.IntegerField(default=0)
    created_on   = models.DateTimeField(auto_now_add=True)
    updated_by   = models.IntegerField(default=0)
    updated_on   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'

class EditingPreference(models.Model):
    service_id  = models.ManyToManyField(Services, through='ServiceEditingPreference')
    name        = models.CharField(max_length=255)
    created_on  = models.DateTimeField(auto_now_add=True)
    created_by  = models.IntegerField(default=0)
    updated_on  = models.DateTimeField(auto_now=True)
    updated_by  = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'editing_preference'

class ServiceEditingPreference(models.Model):
    service_id     = models.ForeignKey(Services, on_delete=models.CASCADE, db_column="service_id")
    preference_id  = models.ForeignKey(EditingPreference, on_delete=models.CASCADE, db_column="preference_id")
    price          = models.DecimalField(decimal_places=2, max_digits=18, default=0.00)
    
    class Meta:
        db_table = 'service_editing_preference'