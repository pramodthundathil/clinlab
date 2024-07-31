from django.db import models
from django.contrib.auth.models import User


class Units(models.Model):
    unit = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True, default= " ")


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    age = models.CharField(max_length=20,null=True)
    gender = models.CharField(max_length=10,null=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class LabDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab_name = models.CharField(max_length=255,null=True, blank=True)
    country = models.CharField(max_length=20,null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    postel_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    logo_of_lab = models.FileField(upload_to='lab_logo', null=True, blank=True)




