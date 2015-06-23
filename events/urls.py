from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^events/new/$', views.EventCreate.as_view(), name='new_event'),
    url(r'^periods/$', views.PeriodIndex.as_view(), name='periods_index'),
]
