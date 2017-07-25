"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from products import views


urlpatterns = [
    url(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    url(r'^detail/(?P<pk>\d+)/$', views.ProductDetail.as_view(), name='detail'),
    url(r'^phone/$', views.Phone.as_view(), name='phone'),
    url(r'^notebook/$', views.Notebook.as_view(), name='notebook'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ProductD.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
