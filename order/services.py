from decimal import Decimal
from django.core.exceptions import ValidationError
from cart.services import CartService
from .models import Order, OrderItem


class OrderService:
    @staticmethod
    def create_order_from_cart(request,guest_data=None):
        cart = CartService.get_or_create_cart(request)
        if not cart.items.exists():
            raise ValidationError("Cart is empty. Cannot create order.")
        order_data = {
            'session_key': None if request.user.is_authenticated else request.session.session_key,
            'billing_address': guest_data.get('billing_address'),
            'city': guest_data.get('city'),
            'postal_code': guest_data.get('postal_code'),
            'country': guest_data.get('country'),
        }
        if request.user.is_authenticated:
            order_data['user'] = request.user
        else:
            order_data['guest_email'] = guest_data.get('email')
            order_data['guest_phone'] = guest_data.get('guest_phone')
        order = Order.objects.create(**order_data)
        
        for item in cart.items.select_related('product'):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
        
        # Clear the cart after creating the order
        cart.items.all().delete()
        return order
    @staticmethod
    def get_users_orders(request):
        if request.user.is_authenticated:
            return Order.objects.filter(user=request.user).prefetch_related('items__product')
        else:
            session_key = request.session.session_key
            if not session_key:
                return Order.objects.none()
            return Order.objects.filter(session_key=session_key).prefetch_related('items__product')
    @staticmethod  
    def get_order_by_id(request, order_id):
        orders = OrderService.get_users_orders(request)
        try:
            return orders.get(id=order_id)
        except Order.DoesNotExist as e:
            raise ValidationError("Order not found ") from e
        
            