from  django import template
from ecommerce.models import Order,OrderProduct
from django.conf import settings
register = template.Library()

@register.filter
def cart_items_count(user):
    if user.is_authenticated:
        ord = Order.objects.filter(user=user,ordered=False)
        if ord.exists():
            return OrderProduct.objects.filter(order=ord[0]).count()

        return 0
    
