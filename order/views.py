from re import I
from rest_framework import viewsets,status
from .serializers import OrderSerializer, CreateOrderSerializer
from rest_framework.response import Response
from order.services import order_query, order_creation
from ecommerce_api.permissions import IsAuthenticatedOrHasSession
from rest_framework.permissions import AllowAny

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