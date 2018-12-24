from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Shop, GoodType, Goods


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        login_name = request.POST.get('username')
        password = request.POST.get('pwd')
        user = authenticate(username=login_name, password=password)

        if user is not None:
            if user.is_superuser is True:
                login(request, user)
                # print('cc',dir(request.session))
                print('cc', request.user.id)
                # 登录成功跳转到主界面
                return redirect(reverse('shop:index'))
            else:
                return render(request, 'shop/login.html', {'msg': '用户名或密码错误'})

        else:
            # 返回登录页面
            return render(request, 'shop/login.html', {'msg': '用户名或密码错误'})

    return render(request, 'shop/login.html', {'msg': ''})


def index(request):
    return render(request, 'shop/goodslist.html')


def goodlist(request):
    return render(request, 'shop/goodslist.html')


def addgoods(request):
    if request.POST == 'POST':
        pass
    return render(request, 'shop/addgoods.html')


def shopinfo(request):
    return render(request, 'shop/shopinfo.html')


def editshop(request):
    shop = Shop.objects.filter(user_id=request.user.id)[0]

    if request.method == 'POST':
        print('ok11')
        shop.name = request.POST.get('name')
        shop.intro = request.POST.get('intro')
        shop.save()
        print('ok')
        return render(request, 'shop/editshop.html', {'shop': shop})
    return render(request, 'shop/editshop.html', {'shop': shop})
