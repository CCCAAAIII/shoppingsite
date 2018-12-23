from django.db import models
import os
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100, default='shopper')
    age = models.IntegerField(default=20)
    gender = models.CharField(default='女', max_length=20)
    header = models.ImageField(upload_to=os.path.join('customer', 'header'), null=True, default='customer/header/1.png')
    phone = models.CharField(max_length=50)
    status = models.IntegerField(default=0)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    receive_name = models.CharField(max_length=50)
    reveive_phone = models.CharField(max_length=50)
    nation = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    county = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    describe = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
