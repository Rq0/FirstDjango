from django.shortcuts import render
from django.views.generic import ListView, DetailView
from rest_framework import generics

from orders.forms import ProductInBasketForm
from products.models import *
from products.serializers import ProductSerializer


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductInBasketForm(initial={
        "product": product_id,
        "is_active": True,
        "session_key": request.session.session_key})
    return render(request, 'products/product.html', locals())


class Phone(ListView):
    model = Product
    context_object_name = 'phones'
    template_name = 'landing/phone.html'

    def get_queryset(self):
        return super(Phone, self).get_queryset().filter(category_id=1)


class Notebook(ListView):
    model = Product
    context_object_name = 'notebooks'
    template_name = 'landing/notebook.html'

    def get_queryset(self):
        return super(Notebook, self).get_queryset().filter(category_id=2)


class ProductDetail(DetailView):
    model = Product


class ProductD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def product(self, product_id):
        product = Product.objects.get(pk=product_id)
        return render(self, 'products/product_detail.html', {'product': product})
