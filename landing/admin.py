# -*- coding: utf-8 -*-
from django.contrib import admin

from landing.models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subscriber._meta.fields]
    list_filter = ["name"]
    exclude = ["email"]  # | fields = ["email"]
    search_fields = ["name", "email"]

    class Meta:
        model = Subscriber


admin.site.register(Subscriber, SubscriberAdmin)
