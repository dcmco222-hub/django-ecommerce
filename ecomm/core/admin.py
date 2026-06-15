from django.contrib import admin
from django.utils.html import format_html

from .models import (Category, Product, Cart, CartItem, Order, OrderItem)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'stock', 'available', 'category', 'image_tag')

    list_filter = ( 'available', 'category')

    search_fields = ( 'name', 'description')

    prepopulated_fields = {
        'slug': ('name',)
    }

    ordering = ('-created_at',)

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;" />',
                obj.image.url
            )
        return "-"

    image_tag.short_description = "Image"