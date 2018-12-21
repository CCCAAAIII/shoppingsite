from django.db import models
import os
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100, default='shopper')
    age = models.IntegerField(default=20)
    gender = models.CharField(default='女', max_length=20)
    header = models.ImageField(upload_to=os.path.join('user', 'header'), null=True)
    phone = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
