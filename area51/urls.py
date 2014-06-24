"""
Application's url pattern registration
"""

from django.conf.urls import patterns, url
from area51 import views
from area51.feeds import LatestEntriesFeed

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^new/$', views.new, name='new'),
    url(r'^list/$', views.list_page, name='list_page'),
    url(r'^moderator/$', views.mod, name='mod'),
    url(r'^u/(?P<username>\w+)/$', views.user, name='user'),
    url(r'^e/(?P<given_id>\w+)/$', views.event, name='event'),
    url(r'^api/data/$', views.data, name='data'),
    url(r'^api/event_list/$', views.event_list, name='event_list'),
    url(r'^api/user_list/$', views.user_list, name='user_list'),
    url(r'^api/adduser/$', views.adduser, name='adduser'),
    url(r'^api/addevent/$', views.addevent, name='addevent'),
    url(r'^api/edituser/$', views.edituser, name='edituser'),
    url(r'^api/checkevent/(?P<given_id>\w+)/$', views.checkevent, name='checkevent'),
    url(r'^api/login/$', views.homelogin, name='homelogin'),
    url(r'^api/logout/$', views.homelogout, name='homelogout'),
    url(r'^api/panel/$', views.panel, name='panel'),
    url(r'^api/panel/categories/$', views.cat_panel, name='cat_panel'),
    url(r'^feed/$', LatestEntriesFeed()),
)
