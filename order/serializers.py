from decimal import Decimal
from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Assuming you have a ProductSerializer
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_amount']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'guest_email', 'guest_phone', 'billing_address', 'city', 'postal_code', 'country', 'status', 'created_at', 'updated_at', 'items', 'total_price']
        read_only_fields = ['status', 'created_at', 'updated_at', 'items', 'total_price']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["total_price"] = Decimal(data["total_price"])
        return data

class CreateOrderSerializer(serializers.ModelSerializer):
    confirm = serializers.BooleanField(write_only=True, required=True)
    class Meta:
        model = Order
        fields = ['guest_email', 'guest_phone', 'billing_address', 'city', 'postal_code', 'country', 'confirm']
    
    def validate(self, attrs):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            if not attrs.get("guest_email"):
                raise serializers.ValidationError("Email is required for guest checkout")
        return attrs
    