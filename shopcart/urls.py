from django.conf.urls import url,include

from shopcart import views
urlpatterns = [
    url(r'^index/$',views.index,name='index'),

]