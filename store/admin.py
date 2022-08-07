from itertools import count, product
from pickletools import read_uint1
from django.db.models.aggregates import Count, Sum, Min, Max, Avg
from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
# Register your models here.

Critically_low = 5
Low = 10
OK = 50


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):

        return [
            ('Critically_low', 'Critically_low'),
            ('Low', 'Low'),
            ('OK', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Critically_low':
            return queryset.filter(inventory__lt=Critically_low)
        if self.value() == 'Low':
            return queryset.filter(inventory__lt=Low)
        if self.value() == 'OK':
            return queryset.filter(inventory__lt=OK)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 5:
            return "Critically low"
        if product.inventory < 10:
            return 'Low'
        if product.inventory < 50:
            return 'OK'
        return "OK"


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'show_orders']
    list_editable = ['membership']
    list_per_page = 10
    list_display_links = ['show_orders']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='show_orders')
    def show_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               })
               )

        return format_html('<a href="{}">{}</a>', url, customer.id)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse('admin:app_Target_model_name_page_name')
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    # list_editable = ['unit_price']
    list_per_page = 10
# admin.site.register(models.Collection)
# admin.site.register(models.Product)
