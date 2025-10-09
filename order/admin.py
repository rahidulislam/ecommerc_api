from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total_amount']
    can_delete = False
    show_change_link = True
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    search_fields = ['user__username', 'guest_email', 'guest_phone']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    inlines = [OrderItemInline]