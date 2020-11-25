from django.conf.urls import url
from . import views #同階層のviewsを読み込む

urlpatterns = [url(r'^$', views.index, name='index')]
