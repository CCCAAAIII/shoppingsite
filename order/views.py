from django.shortcuts import render
from shopcart.models import CartItem
from customer.models import User, Address
from datetime import datetime
from order.models import Order,OrderItem

# Create your views here.
def index(request):
    if request.method == 'POST':
        address = Address.objects.filter(user_id=request.user.id)[0]
        items = request.POST.getlist('check_list')
        item_list = []
        total_money = 0
        for i in items:
            cart = CartItem.objects.get(id=i)
            total_money += cart.goods.price * cart.count
            print(total_money)
            item_list.append(cart)
            # print(cart.goods.image)
            # print(i)

        return render(request, 'order/orderSubmit.html',
                      {'item_list': item_list, 'item_count': len(items), 'total_money': total_money, 'address': address,
                       'items': items})


def generateorder(request):

    items = request.POST.getlist('cartitemid')
    receive_name = request.POST.get('receivename')
    receivephone = request.POST.get('receivephone')
    address = request.POST.get('address')
    totalmoney = request.POST.get('totalmoney')
    remark = request.POST.get('remark')
    order_time = datetime.now()
    status = 0
    o = Order.objects.create(receive_name=receive_name,receive_phone=receivephone,
                         receive_address=address,receive_remark=remark,total_money=totalmoney,order_time=order_time,user_id=request.user.id,status=status)
    # CartItem.objects.get(id=32)
    # print(type(items))
    print(items)
    for i in items:
        print(i)
        try:
            print(i)
            item = CartItem.objects.get(id=i)
            goods = item.goods
            goods.stock -= item.count
            goods.sale_count += item.count
            goods.save()
            item.save()
            OrderItem.objects.create(name=goods.name, price=goods.price, count=item.count,
                                     money=item.count * goods.price, order_id=o.id)
            item.delete()
        except Exception as  e:
            print(e)

    return render(request, 'order/orderok.html')
