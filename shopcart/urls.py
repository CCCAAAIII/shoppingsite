from django.conf.urls import url,include

from shopcart import views
urlpatterns = [
    # 购物车详情
    url(r'^mycart/$',views.index,name='mycart'),
    # 删除购物车item
    url(r'^deletecartitem/$', views.deleteitem, name='deleteitem'),

]