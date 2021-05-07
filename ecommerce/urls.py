from django.urls import path

from .views import (checkout,productView,productDetail,add_to_cart,remove_from_cart)

app_name = "ecommerce"

urlpatterns = [
        path('', productView.as_view(), name='home'),
        path('checkout/', checkout, name='checkout'),
        path('product/<slug>/', productDetail.as_view(), name='productDetail'),
        path('add_to_cart/<slug>', add_to_cart, name="add_to_cart"),
        path('remove_from_cart/<slug>',remove_from_cart,name='remove_from_cart')
    ]
