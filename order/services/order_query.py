from django.core.exceptions import ValidationError
from order.models import Order


class OrderQueryService:
    """
    Get all orders for authenticated user or session-based guest.
    """

    @staticmethod
    def get_user_orders(request):
        """
        Retrieves all orders for the current user or session-based guest.
        Returns an empty queryset if no session exists for anonymous users.
        """
        if request.user.is_authenticated:
            return Order.objects.filter(user=request.user).prefetch_related(
                "items__product"
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                return Order.objects.none()
            return Order.objects.filter(session_key=session_key).prefetch_related(
                "items__product"
            )

    @staticmethod
    def get_order_by_id(request, order_id):
        """
        Retrieves a specific order by ID for the current user or session.
        Raises ValidationError if the order does not exist or does not belong to the user/session.
        """
        orders = OrderQueryService.get_user_orders(request)
        try:
            return orders.get(id=order_id)
        except Order.DoesNotExist as e:
            raise ValidationError("Order not found") from e
    @staticmethod
    def get_order_by_email(request, email):
        try:
            return Order.objects.filter(guest_email=email).first()
        except Order.DoesNotExist as e:
            raise ValidationError("Order not found") from e
