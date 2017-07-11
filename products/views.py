from django.shortcuts import render

from orders.forms import ProductInBasketForm
from products.models import *


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductInBasketForm(initial={
        "product": product_id,
        "is_active": True,
        "session_key": request.session.session_key})
    return render(request, 'products/product.html', locals())
