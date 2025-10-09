from django.core.exceptions import ValidationError
from order.models import Order


class OrderValidator:
    @staticmethod
    def validate_no_pending_order(request, guest_data=None):
        """
        Prevent multiple pending orders for same user/session/guest.
        """
        filters = {}
        if request.user.is_authenticated:
            filters["user"] = request.user
        elif request.session.session_key:
            filters["session_key"] = request.session.session_key
        else:
            guest_email = guest_data.get("guest_email")
            if guest_email:
                filters["guest_email"] = guest_email

        # Prevent duplicate pending orders for the same user/session/guest
        if (
            filters
            and Order.objects.filter(
                status=Order.STATUS_CHOICES.PENDING, **filters
            ).exists()
        ):
            raise ValidationError(
                "You already have a pending order. Please complete it first."
            )
