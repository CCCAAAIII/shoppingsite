from django.conf.urls import url,include

from shop import views
urlpatterns = [
    url(r'^index/',views.index,name='index'),
    url(r'^addgoods/',views.addgoods,name='addgoods'),
    url(r'^login/',views.login_view,name='login_view'),
    url(r'^shopinfo/',views.shopinfo,name='shopinfo'),
    url(r'^goodlist/',views.goodlist,name='goodlist'),
    url(r'^editshop/',views.editshop,name='editshop'),
]