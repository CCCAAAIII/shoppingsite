from django.shortcuts import render
from .models import CartItem
from shop.models import Goods,GoodType

# Create your views here.
def index(request):
    user_id = request.user.id
    if request.method == 'POST':
        pass
    else:
        cart = CartItem.objects.filter(user_id=user_id)
        return render(request, 'shopcart/shoppingcart.html', {'cart': cart})
