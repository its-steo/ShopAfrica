from django.contrib import admin
from .models import Order, OrderItem, Payment
from django.utils.html import format_html

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'total_amount', 'order_status', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    inlines = [OrderItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'method', 'submitted_at', 'screenshot_preview']
    readonly_fields = ['order', 'method', 'screenshot', 'submitted_at', 'screenshot_preview']

    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" width="150" style="border: 1px solid #ccc;" />', obj.screenshot.url)
        return "No Screenshot"

    screenshot_preview.short_description = 'Screenshot Preview'
