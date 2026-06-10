from django.contrib import admin
from .models import Category, Product, Cart, CartItem
from django.utils.html import format_html

admin.site.register(Cart)
admin.site.register(CartItem)

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'category', 'image_tag')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    # For previewing Images in admin

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;" />', obj.image.url)
        return "-"

    image_tag.short_description = "Image"

# Ordering by time and date created
class ProductAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)

    