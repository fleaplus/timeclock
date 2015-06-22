from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.account_confirm, name='account_confirm'),
    url(r'^', include('django.contrib.auth.urls')),
]
