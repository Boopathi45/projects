from django.db import models

# Create your models here.


class Profile(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    previouswork = models.CharField(max_length=200)
    skills = models.TextField(max_length=2000)
