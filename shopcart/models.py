from django.db import models
from customer.models import User
from shop.models import Goods
# Create your models here.
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User)
