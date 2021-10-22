from django.urls import path
from django.conf.urls import url
from django.contrib import admin

from .views import (
    get_all_foods_and_categorys,
    PizzaListAPIView,
    OpenOrderListAPIView,
    OrderListAPIView,
    SaboresListAPIView,
    BebidasListAPIView,
    OrderUpdateAPIView,
    OrderDeleteAPIView,
    add_cart,
    OpenUpdateAPIView
)


urlpatterns = [

    url(r'^$', PizzaListAPIView.as_view(), name='list'),

    url(r'^todas/$', get_all_foods_and_categorys, name='todas'),
    url(r'^add-cart/$', add_cart, name='add-cart'),
    url(r'^all-orders/$', OrderListAPIView.as_view(), name='orders'),
    url(r'^bebidas/$', BebidasListAPIView.as_view(), name='bebidas'),
    url(r'^sabores/$', SaboresListAPIView.as_view(), name='sabores'),
    url(r'^open-orders/$', OpenOrderListAPIView.as_view(), name='orders'),
    url(r'^order/(?P<id>[\w-]+)/edit/$',
        OrderUpdateAPIView.as_view(), name='update'),
    url(r'^order/(?P<id>[\w-]+)/delete/$',
        OrderDeleteAPIView.as_view(), name='delete'),
    url(r'^open/$',
        OpenUpdateAPIView.as_view(), name='open'),
    url(r'^open/(?P<id>[\w-]+)/edit/$',
        OpenUpdateAPIView.as_view(), name='open-update'),

]
