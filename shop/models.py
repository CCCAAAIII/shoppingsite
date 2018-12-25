from django.db import models
# from customer.models import User
from customer.models import User

# Create your models here.
class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    intro = models.CharField(max_length=100)
    open_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class GoodType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    type_desc = models.CharField(max_length=100)


class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    normal_price = models.FloatField(default=100)


    price = models.FloatField()
    stock = models.IntegerField()
    sale_count = models.IntegerField(default=0)
    add_time = models.DateTimeField()
    desc = models.CharField(max_length=100)
    good_type = models.ForeignKey(GoodType)
    good_store = models.ForeignKey(Shop)
    is_sale = models.BooleanField(default=True)
    image = models.ImageField(upload_to='shop/goodimages',default='shop/1.png')



class GoodImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='shop/goodimages',default='shop/1.png')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
