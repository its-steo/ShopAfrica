from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('product', 'quantity', 'unit_price', 'total_price')
    fields = ('product', 'quantity', 'unit_price', 'total_price', 'selected_image_url')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'is_active', 'created_at')
    inlines = [CartItemInline]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'unit_price', 'total_price', 'selected_image_url')
    readonly_fields = ('unit_price', 'total_price')
    list_filter = ('cart', 'product')
    search_fields = ('product__name', 'cart__session_key')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)