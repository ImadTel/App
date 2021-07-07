from django.urls import path

from .views import (checkout,productView,productDetail,add_to_cart,remove_from_cart,cart_view,update_view)

app_name = "ecommerce"

urlpatterns = [
        path('', productView.as_view(), name='home'),
        path('checkout/', checkout, name='checkout'),
        path('product/<slug>/', productDetail.as_view(), name='productDetail'),
        path('add_to_cart/<slug>', add_to_cart, name="add_to_cart"),
        path('cart/<slug>&<quantity>', add_to_cart, name="cart_view_res"),
        path('remove_from_cart/<slug>',remove_from_cart,name='remove_from_cart'),
        path('cart/',cart_view,name='cart_view'),
        path('update_item/<pk>',update_view.as_view(),name="update_item")
    ]
