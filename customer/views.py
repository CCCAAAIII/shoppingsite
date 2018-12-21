from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import User
from django.db.models import Q
from io import BytesIO
from django.contrib.auth.backends import ModelBackend
from . import utils
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired


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
@login_required()
def index(request):
    pass


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('passwordB')
        phone = request.POST.get('phone')
        if request.session['check_code'] == request.POST.get('code'):
            try:
                username='customer'+email
                user = User.objects.create_user(email=email, password=password, phone=phone, username=username)
                user.is_active = False
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

    return render(request, 'customer/register.html', {'msg': 'ok'})


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
        return redirect(reverse('customer:login'))
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
