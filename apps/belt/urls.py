from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/create$', views.createuser),
    url(r'^user/login$', views.login),
    url(r'^travels$', views.show),
    url(r'^travels/add$', views.addtrip),
    url(r'^travels/join/(?P<id>\d+)$', views.join),
    url(r'^trip/create$', views.createtrip),
    url(r'^logout$', views.logout),
    url(r'^travels/destination/(?P<id>\d+)$', views.showtrip),
]
