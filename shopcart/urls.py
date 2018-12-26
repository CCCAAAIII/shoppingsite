from django.conf.urls import url,include

from shopcart import views
urlpatterns = [
    url(r'^mycart/$',views.index,name='mycart'),

]