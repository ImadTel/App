from django.urls import path

from .views import (checkout,productView,productDetail)

app_name = "ecommerce"

urlpatterns = [
        path('', productView.as_view(), name='home'),
        path('checkout/', checkout, name='checkout'),
        path('product/<slug>/', productDetail.as_view(), name='productDetail'),

    ]
