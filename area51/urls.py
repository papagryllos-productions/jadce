from django.conf.urls import patterns, url

from area51 import views
from area51.feeds import LatestEntriesFeed

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^u/(?P<username>\w+)/$', views.user, name='user'),
    url(r'^api/data/$', views.data, name='data'),
    url(r'^feed/$', LatestEntriesFeed()),
)
