from django.conf.urls import patterns, url
from area51 import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^(?P<username>\w+)/$', views.details, name='details'),
)
