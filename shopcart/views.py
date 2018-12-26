from django.shortcuts import render
from .models import CartItem
from shop.models import Goods, GoodType
from django.http import JsonResponse
from datetime import datetime


# Create your views here.
def index(request):
    user_id = request.user.id
    if request.method == 'POST':
        pass
    else:
        cart = CartItem.objects.filter(user_id=user_id)
        return render(request, 'shopcart/shoppingcart.html', {'cart': cart})


def deleteitem(request):
    id = request.GET.get('id')
    try:
        # print(id,type(id))
        item = CartItem.objects.get(id=id)
        # print(item)
        item.delete()
        return JsonResponse({'msg': 'ok'})
    except Exception as e:
        return JsonResponse({'msg': 'error'})


def itemcount(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    try:
        item = CartItem.objects.get(id=id)
        item.count = count
        item.add_time = datetime.now()
        item.save()
        return JsonResponse({'msg': 1})
    except Exception as e:
        return JsonResponse({'msg': 0})
