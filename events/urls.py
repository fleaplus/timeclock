from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.EventCreate.as_view(), name='new_event')
]
