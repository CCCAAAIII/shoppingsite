from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.register, name='register'),
    # 激活
    url(r'active/(?P<token>.*)$',views.active,name='active'),
    # 获得验证码图片
    url(r'^getcheckcode/$', views.check_code, name='checkcode')
]
