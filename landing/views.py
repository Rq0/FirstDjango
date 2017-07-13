import datetime
from django.shortcuts import render

from products.models import ProductImage
from .forms import SubscribersForm


def landing(request):
    name = 'rq0'
    form = SubscribersForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        print(form.cleaned_data["name"])
        new_form = form.save()
    return render(request, 'landing/landing.html', locals())


def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    products_images_phones = products_images.filter(product__category__id=1)
    products_images_laptops = products_images.filter(product__category__id=2)
    date = datetime.datetime.now().month
    products_images_new = products_images.filter(product__created__month=date)
    return render(request, 'landing/home.html', locals())
