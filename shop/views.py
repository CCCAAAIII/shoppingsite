from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from .models import Shop, GoodType, Goods, GoodImage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


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

@login_required(login_url='shop:login_view')
def index(request):
    return render(request, 'shop/goodslist.html')


def goodlist(request):
    goods = Goods.objects.all()
    return render(request, 'shop/goodslist.html', {'goods': goods})


@csrf_exempt
def addgoods(request):
    types = GoodType.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            type = request.POST.get('type')
            image = request.FILES['input_image']
            normal_price = request.POST.get('normal_price')
            is_sale = request.POST.get('is_sale')
            desc = request.POST.get('desc')
            good_store_id = 1

            good = Goods.objects.create(name=name, normal_price=normal_price, price=price, stock=stock,
                                        good_store_id=good_store_id,
                                        add_time=datetime.now(), is_sale=is_sale, desc=desc, good_type_id=type,
                                        image=image)
            # GoodImage.objects.create(image=image, goods_id=good.id)
            # print(a)
            print('ok')
            msg = '添加成功，您可以继续添加'
            return render(request, 'shop/addgoods.html', {'types': types, 'msg': msg})
        except Exception as e:
            msg = '遇到了点错误，请尝试重新添加商品'
            return render(request, 'shop/addgoods.html', {'types': types, 'msg': msg})
    msg = ''
    return render(request, 'shop/addgoods.html', {'types': types, 'msg': msg})


# @csrf_exempt
def goodsedit(request, id):
    types = GoodType.objects.all()
    if request.method == 'POST':
        try:
            good = Goods.objects.get(id=id)
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            type = request.POST.get('type')
            try:
                image = request.FILES['input_image']
            except:
                image = good.image
            normal_price = request.POST.get('normal_price')
            is_sale = request.POST.get('is_sale')
            desc = request.POST.get('desc')
            good_store_id = 1
            good.name = name
            good.normal_price = normal_price
            good.price = price
            good.stock = stock
            good.good_store_id = good_store_id
            good.is_sale = is_sale
            good.desc = desc
            good.good_type_id = type
            good.image = image
            good.save()
            print('ok')
            msg = '修改成功'
            return render(request, 'shop/editgoods.html', {'good': good, 'types': types, 'msg': msg, 'image': image})

        except Exception as e:
            msg = '遇到了点错误，请尝试重新'
            # return redirect(reverse("shop:goodsedit",id, {'types': types, }))
    msg = ''
    good = Goods.objects.get(id=id)
    # image = GoodImage.objects.get(goods_id=id)
    return render(request, 'shop/editgoods.html', {'good': good, 'types': types, 'msg': msg})


def shopinfo(request):
    return render(request, 'shop/shopinfo.html')


def goodsdelete(request, id):
    try:
        rs = Goods.objects.filter(id=id)
        if len(rs) != 0:
            goods = rs[0]
            goods.delete()
            msg = {'msg': 'delete ok'}
        else:
            msg = {'msg': 'goods not exist'}
        return JsonResponse(msg)
    except Exception as e:
        print(e)
        msg = {'msg': 'error'}
        return JsonResponse(msg)


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
def logout_view(request):
    logout(request)
    return redirect(reverse('shop:login_view'))