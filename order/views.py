
from email.policy import HTTP
from rest_framework import viewsets,status
from rest_framework.decorators import api_view,permission_classes
from order.services.payment_service import PaymentService
from order.models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from rest_framework.response import Response
from order.services import order_query, order_creation
from ecommerce_api.permissions import IsAuthenticatedOrHasSession
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json, stripe

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post',]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return super().get_serializer_class()
    def get_queryset(self):
        return order_query.OrderQueryService.get_user_orders(self.request)

    def create(self, request, *args, **kwargs):
        """
        Creates an order from the user's or guest's cart.
        Transfers all cart items to the new order, updates product stock, and clears the cart.
        Raises ValidationError if the cart is empty or a pending order exists.
        Returns the created order in JSON format.
        """
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        confirm = serializer.validated_data.pop('confirm', False)
        if not confirm:
            return Response({'error': 'You must confirm the order.'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user or not request.session:
            print("Guest user")
        try:
            order = order_creation.OrderCreator.create_order_from_cart(request, guest_data=serializer.validated_data)
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@extend_schema(
    description="Create a Stripe Checkout Session for an order",
    parameters=[
        OpenApiParameter(
            name="order_id",
            location=OpenApiParameter.QUERY,
            type=int,
            description="ID of the pending order",
        ),
    ],
    responses={
        200: {'type': 'object', 'properties': {'url': {'type': 'string'}}},
        400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
    }
)
@api_view(['POST'])

def create_checkout_session(request):
    order_id = request.data.get('order_id') or request.query_params.get('order_id')
    if not order_id:
        return Response({'error': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        session = PaymentService.create_checkout_session(request, order_id)
        return Response({'url': session.url}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@require_http_methods(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe.api_key
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # handle the event
    if event.type == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)
    return HttpResponse(status=200)

def handle_checkout_session(session):
    """Update order status after successful payment"""
    metadata = session.get('metadata',{})
    order_id = metadata.get('order_id')
    if not order_id:
        return
    try:
        order = Order.objects.get(id=order_id)
        if order.status == Order.STATUS_CHOICES.PENDING:
            order.status = Order.STATUS_CHOICES.CONFIRMED
            order.save()
    except Order.DoesNotExist:
        pass


def payment_success(request):
    checkout_session_id = request.query_params.get('session_id')
    return HttpResponse(f"Payment successful with session ID: {checkout_session_id}")
