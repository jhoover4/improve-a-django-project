from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='menu_list'),
    url(r'^menu/new/$', views.create_edit_menu, name='menu_create'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.create_edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/$', views.item_list, name='item_list'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/item/new/$', views.create_edit_item, name='item_create'),
    url(r'^menu/item/(?P<pk>\d+)/edit$', views.create_edit_item, name='item_edit'),
]
