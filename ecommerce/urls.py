from django.urls import path

from .views import products,checkout

app_name = "ecommerce"

urlpatterns = [
        path('', products, name='home'),
        path('checkout/', checkout, name='checkout'),
    ]
