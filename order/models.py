from django.db import models
from customer.models import User
# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    receive_name = models.CharField(max_length=50,verbose_name='收货人')
    receive_address = models.CharField(max_length=150,verbose_name='收货地址')
    receive_phone = models.CharField(max_length=50,verbose_name='收货人电话')
    receive_remark = models.CharField(max_length=150,verbose_name='备注信息')
    total_money = models.FloatField()
