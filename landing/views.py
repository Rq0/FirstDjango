from django.shortcuts import render

from .forms import SubscribersForm


def landing(request):
    name = 'rq0'
    form = SubscribersForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form = form.save()
    return render(request, 'landing/landing.html', locals())
