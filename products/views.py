from django.shortcuts import render
from django.views.generic import UpdateView
from products.models import *
from orders.forms import ProductInBasketForm


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductInBasketForm(initial={
        "product": product_id,
        "is_active": True,
        "session_key": request.session.session_key})
    return render(request, 'products/product.html', locals())
