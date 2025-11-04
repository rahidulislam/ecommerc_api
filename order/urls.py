from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, create_checkout_session, stripe_webhook,payment_success

app_name = 'order'
router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')
urlpatterns = [
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('payment/success/', payment_success, name='payment-success'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
urlpatterns += router.urls