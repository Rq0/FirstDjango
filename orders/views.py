from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from orders.forms import CheckoutContactForm, ProductInBasketForm
from orders.models import ProductInBasket, Order, ProductInOrder
from products.models import Product


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects. \
            get_or_create(session_key=session_key,
                          product_id=product_id,
                          is_active=True,
                          defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    # common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


class BasketAddExample(CreateView):
    model = ProductInBasket
    form_class = ProductInBasketForm
    template_name = 'products/product.html'

    def get(self, request, *args, **kwargs):
        raise NotImplementedError

    def form_valid(self, form):
        try:
            self.object = self.model.objects.get(
                product_id=self.kwargs.get('product_id'),
                session_key=self.request.session.session_key,
                is_active=True,
                order__isnull=True,
            )
        except self.model.DoesNotExist:
            self.object = self.model(**form.cleaned_data)
        else:
            self.object.nmb += form.cleaned_data.get("nmb", 0)

        self.object.save()
        qs = ProductInBasket.objects. \
            filter(session_key=self.request.session.session_key,
                   is_active=True, order__isnull=True)
        kek = [{"id": item.id,
                "name": item.product.name,
                "price_per_item": item.price_per_item,
                "nmb": item.nmb} for item in qs]
        return JsonResponse({
            "products": kek,
            "products_total_nmb": form.cleaned_data.get("nmb", 0)
        })

    def form_invalid(self, form):
        return JsonResponse({"fail": form.errors})


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)

    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("form valid")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("form not valid")
    return render(request, 'orders/checkout.html', locals())


class OrderList(TemplateView):
    template_name = "landing/order_report.html"

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        orders = Order.objects.all()
        context['orders'] = orders
        products_in_orders = ProductInOrder.objects.all()
        context['products_in_orders'] = products_in_orders
        context['products'] = Product.objects.all()

        context['avg_total_price'] = sum([i.total_price for i in orders]) / len(orders)

        total_price = []
        for i in orders:
            total_price.append(i.total_price)
        sum(total_price) / len(orders)

        context['avg_product_count'] = sum([i.nmb for i in products_in_orders]) / len(products_in_orders)
        return context
