from django.db import transaction
from django.core.exceptions import ValidationError
from cart.services import CartService
from order.models import Order, OrderItem
from order.services.order_validation import OrderValidator
from order.services.stock_management import StockManager


class OrderCreator:
    @staticmethod
    @transaction.atomic
    def create_order_from_cart(request, guest_data=None):
        """
        Creates an order from the user's or guest's cart.
        Transfers all cart items to the new order, updates product stock, and clears the cart.
        Raises ValidationError if the cart is empty or a pending order exists.
        """
        cart = CartService.get_or_create_cart(request)
        if not cart.items.exists():
            raise ValidationError("Cart is empty. Cannot create order.")

        # Validate no pending order exists
        OrderValidator.validate_no_pending_order(request, guest_data)

        # Prepare order data
        order_data = {
            "session_key": None
            if request.user.is_authenticated
            else request.session.session_key,
            "billing_address": guest_data.get("billing_address"),
            "city": guest_data.get("city"),
            "postal_code": guest_data.get("postal_code"),
            "country": guest_data.get("country"),
        }
        if request.user.is_authenticated:
            order_data["user"] = request.user
        else:
            order_data["guest_email"] = guest_data.get("guest_email")
            order_data["guest_phone"] = guest_data.get("guest_phone")

        # Create the order
        order = Order.objects.create(**order_data)

        # Transfer each cart item to the order and update product stock
        for item in cart.items.select_related("product"):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            StockManager.deduct_product_stock(item.product, item.quantity)

        # Clear the cart after creating the order
        cart.items.all().delete()
        return order
