from django.conf.urls import url,include

from shop import views
urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^addgoods/$',views.addgoods,name='addgoods'),
    url(r'^login/$',views.login_view,name='login_view'),
    url(r'^shopinfo/$',views.shopinfo,name='shopinfo'),
    url(r'^goodlist/$',views.goodlist,name='goodlist'),
    url(r'^editshop/$',views.editshop,name='editshop'),
    url(r'goodsdelete/(\d+)$',views.goodsdelete,name='goodsdelete'),
    url(r'goodsedit/(\d+)$',views.goodsedit,name='goodsedit'),
    url(r'^logout$',views.logout_view,name='logout_view'),
    url(r'^order/$',views.order,name='order_view'),
]