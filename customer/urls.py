from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.register, name='register'),
    # 激活
    url(r'active/(?P<token>.*)$', views.active, name='active'),
    # 获得验证码图片
    url(r'^getcheckcode/$', views.check_code, name='checkcode'),
    # 登录
    url(r'^login/$', views.login_view, name='login_view'),
    # 网站主页
    url(r'^index/$', views.index, name='index'),
    # 个人中心
    url(r'^personalcenter/$', views.personalcenter, name='personalcenter'),
    # 异步验证用户名是否存在
    url(r'^checkusername/$', views.checkusername, name='checkusername'),
    # 收货地址管理
    url(r'^address/$',views.address,name='address'),
    # 商品详情
    url(r'^productitem/(\d+)$',views.productitem,name='productitem'),
    # 添加购物车
    url(r'^additem/$',views.additem,name='additem'),
    # 退出
    url(r'^logout/$',views.login_view,name='logout_view'),
    # 我的订单
    url(r'^myorder/$',views.myorder,name='myorder'),
    # url(r'^getcartcount/$', views.getcartcount),

]
