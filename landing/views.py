import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import ProductImage, Product
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
