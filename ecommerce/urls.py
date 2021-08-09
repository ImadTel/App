from django.urls import path

from django.conf import settings



from .views import (checkout,productView,productDetail,
                    add_to_cart,remove_from_cart,cart_view,
                    update_view,remove_product_from_cart,
                    Checkout_view,PayementView,CreateCheckoutSession,
                    success_payment,cancel_payment,
                    stripe_webhook,
                    response_with_category,
                    search,
                    insert_comment,
                    )

app_name = "ecommerce"

urlpatterns = [
        path('', productView.as_view(), name='home'),
        path('checkout/', Checkout_view.as_view(), name='checkout'),
        path('product/<slug>/', productDetail.as_view(), name='productDetail'),
        path('add_to_cart/<slug>', add_to_cart, name="add_to_cart"),
        path('cart/<slug>&<quantity>', add_to_cart, name="cart_view_res"),
        path('remove_from_cart/<slug>',remove_from_cart,name='remove_from_cart'),
        path('cart/',cart_view,name='cart_view'),
        path('update_item/<pk>',update_view.as_view(),name="update_item"),
        path('delete_item/slg=<slug>',remove_product_from_cart,name="remove_product_from_cart_view"),
        path('payment/<payement_method>/',PayementView.as_view(),name='payment_method'),
        path('create_checkout_session/',CreateCheckoutSession.as_view(),name='create_checkout_session'),
        path('success/',success_payment,name='success_payment'),
        path('cancel/',cancel_payment,name='cancel_payment'),
        path('stripe/webhook/',stripe_webhook,name='stripe_webhook'),
        path('<category>/',response_with_category,name='response_with_category'),
        path('search',search,name='search_products'),
        path('insert_comment',insert_comment,name="insert_comment")
            ]

