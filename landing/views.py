import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from orders.models import Order, ProductInOrder
from products.models import ProductImage, Product
from .forms import SubscribersForm


def landing(request):
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


class OrderList(TemplateView):
    template_name = "landing/order_report.html"

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['products_in_orders'] = ProductInOrder.objects.all()
        context['products'] = Product.objects.all()

        avg_total_price = 0
        for order in ProductInOrder.objects.all():
            avg_total_price += order.total_price
        context['avg_total_price'] = avg_total_price / Order.objects.count()

        avg_product_count = 0
        for product in ProductInOrder.objects.all():
            avg_product_count += product.nmb
        context['avg_product_count'] = avg_product_count / ProductInOrder.objects.count()

        return context

# model = Order
# context_object_name = 'orders'
# template_name = 'landing/order_report.html'
#
# def get_queryset(self):
#     return super(OrderList, self).get_queryset()
