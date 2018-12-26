from django.conf.urls import url

from order import views
urlpatterns = [
url(r'^ordersubmit',views.index,name='ordersubmint'),
url(r'^generateorder',views.generateorder,name='generateorder'),
]