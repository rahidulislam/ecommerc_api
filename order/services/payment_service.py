from order.models import Order
import stripe

class PaymentService:
    @staticmethod
    def create_checkout_session(request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist as e:
            raise ValueError("Order not found") from e
        if order.status!=Order.STATUS_CHOICES.PENDING:
            raise ValueError("Order is not pending")
        try:
            session = stripe.checkout.Session.create(
                payment_method_types =["card"],
                line_items=[{
                    'price_data':{
                        'currency':'usd',
                        'product_data':{
                            'name': f"Order #{order.id}",
                        },
                        'unit_amount': int(order.total_price*100),
                    },
                    'quantity':1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    "api/orders/payment/success/?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=request.build_absolute_uri(
                    'payment/canceled/'
                ),
                metadata={
                    'order_id':order.id,
                    'user_id':request.user.id if request.user.is_authenticated else None
                }

            )
            return session
        except stripe.error.StripeError as e:
            raise ValueError("Error creating checkout session") from e
        
