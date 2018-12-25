from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Address
from django.db.models import Q
from datetime import datetime
from io import BytesIO
from django.contrib.auth.backends import ModelBackend
from . import utils
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from shop.models import Shop, Goods, GoodImage, GoodType
from django.core.cache import cache
from shopcart.models import CartItem


class CustomBackend(ModelBackend):
    """验证用户 让用户可以使用邮箱登陆"""

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 做并集进行查询  使用Q
            print(username)
            user = User.objects.get(Q(username=username) | Q(email=username))
            # 先查user 然后调用方法去比较密码
            if user.check_password(password):
                return user
        except Exception as err:
            return None


# Create your views here.


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('passwordB')
        phone = request.POST.get('phone')
        rs = User.objects.filter(email=email)

        if request.session['check_code'] == request.POST.get('code'):
            if len(rs) > 0:
                return render(request, 'customer/register.html', {'msg': '用户名已存在'})
            else:
                try:
                    username = 'customer' + email
                    user = User.objects.create_user(email=email, password=password, phone=phone, username=username,
                                                    is_active=False)

                    serializer = Serializer(settings.SECRET_KEY, 3600)
                    info = {'confirm': user.id}
                    # 返回bytes类型
                    token = serializer.dumps(info)
                    # str
                    token = token.decode()

                    # 保存成功，发送邮件
                    m_title = "购酒网账号激活邮件"
                    html_message = """
                                       <h1>%s, 欢迎您成为天天生鲜注册会员</h1>
                                      请点击一下链接激活您的账号(7小时之内有效)<br/>
                                        <a href="http://127.0.0.1:8000/customer/active/%s">http://127.0.0.1:8000/user/active/%s</a>
                                     """ % (username, token, token)

                    m_msg = ''
                    try:
                        send_mail(m_title, m_msg, settings.EMAIL_FROM, [email], html_message=html_message)
                        return render(request, "customer/register.html", {"msg": "恭喜您，注册成功，请登录邮箱激活账号！！"})
                    except Exception as e:
                        print(e)
                        return render(request, "customer/register.html", {"msg": "恭喜您，注册成功，邮箱发送失败，请点击重新发送"})
                except Exception as e:
                    print(e)
                    return render(request, "customer/register.html", {"msg": "注册失败，请重新注册，或者联系管理员"})

    return render(request, 'customer/register.html', {'msg': ''})


def active(request, token):
    """激活用户"""
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        # 解密
        info = serializer.loads(token)
        # 获取待激活用户id
        user_id = info['confirm']
        # 激活用户
        user = User.objects.get(id=user_id)
        user.is_active = 1
        user.save()

        # 跳转登录页面
        return redirect(reverse('customer:login_view'))
    except SignatureExpired as e:
        # 激活链接已失效
        # 实际开发: 返回页面，让你点击链接再发激活邮件
        return HttpResponse('激活链接已失效')


def check_code(request):
    """验证码"""
    f = BytesIO()
    img, code = utils.create_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


def login_view(request):
    """登录"""
    if request.method == 'POST':
        login_name = request.POST.get('username')
        password = request.POST.get('pwd')
        user = authenticate(username=login_name, password=password)

        if user is not None:
            login(request, user)
            # print('cc',dir(request.session))
            print('cc', request.user.id)
            # 登录成功跳转到主界面

            return redirect(reverse('customer:index'))
        else:

            # 返回登录页面
            return render(request, 'customer/login.html', {'msg': '用户名或密码错误'})

    return render(request, 'customer/login.html', {'msg': ''})


def index(request):
    goods = Goods.objects.filter(good_type_id=1)
    images = GoodImage.objects.all()
    return render(request, 'customer/index.html', {'goods': goods, 'images': images})


@login_required(login_url='customer/login/')
def personalcenter(request):
    id = request.user.id
    if request.method == 'POST':
        try:

            # print('cccccc')
            user = User.objects.filter(id=id)[0]
            # print('ddd')
            try:
                head_image = request.FILES['head_image']
            except Exception as e:
                head_image = user.header
            # print(head_image)
            # print('cccccc')

            email = request.POST.get('email')
            nickname = request.POST.get('nickname')
            username = request.POST.get('username')
            gender = request.POST.get('sex')
            user.header = head_image
            user.email = email
            user.nickname = nickname
            user.username = username
            user.gender = gender
            user.save()
            # print('dddddd')
            return redirect(reverse('customer:personalcenter'))
        except Exception as e:
            print(e)

    try:
        user = User.objects.filter(id=id)[0]
        print(request.user.header)
        return render(request, 'customer/personalcenter.html', {'user': user})
    except Exception as e:
        print(e)
        return redirect(reverse('customer:index'))


@csrf_exempt
def checkusername(request):
    username = request.POST.get('username')

    users = User.objects.all()

    rs = users.filter(username=username)
    print('username', username)
    print(len(rs))
    if len(rs) == 0:
        msg = 0
    else:
        msg = 1
    return JsonResponse({'msg': msg})


def address(request):
    if request.method == 'POST':
        receive_name = request.POST.get('receivename')
        receive_phone = request.POST.get('phone')
        nation = request.POST.get('nation')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        street = request.POST.get('street')
        describ = request.POST.get('describe')
        user_id = request.user.id
        Address.objects.create(receive_name=receive_name, reveive_phone=receive_phone, nation=nation,
                               province=province, city=city, county=county, street=street, describe=describ,
                               user_id=user_id)
    rs = Address.objects.filter(user_id=request.user.id)
    address = None
    if len(rs) == 0:
        return render(request, 'customer/address.html', {'address': address})
    else:
        address = rs[0]
        return render(request, 'customer/address.html', {'address': address})


def productitem(request, id):
    good = Goods.objects.filter(id=id)[0]
    type = GoodType.objects.get(id=good.good_type_id).type_name

    return render(request, 'customer/productitem.html', {'good': good, 'type': type})


def additem(request):
    good_id = request.GET.get('id')
    count = request.GET.get('count')
    time = datetime.now()
    try:
        # 从数据库查询用户是否已加入该商品，如果有则累加数量如果没有则新建一个购物车记录对象
        
        CartItem.objects.create(goods_id=good_id, count=count, user_id=request.user.id, add_time=time)
    except Exception as e:
        print(e)
    return JsonResponse({'msg': 'ok'})
