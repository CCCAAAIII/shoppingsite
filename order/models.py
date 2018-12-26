from django.db import models
from customer.models import User


# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    receive_name = models.CharField(max_length=50, verbose_name='收货人')
    receive_address = models.CharField(max_length=150, verbose_name='收货地址')
    receive_phone = models.CharField(max_length=50, verbose_name='收货人电话')
    receive_remark = models.CharField(max_length=150, verbose_name='备注信息')
    order_time = models.DateTimeField()
    total_money = models.FloatField()
    status = models.IntegerField(default=0)



class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.FloatField()
    count = models.IntegerField()
    money = models.FloatField()

