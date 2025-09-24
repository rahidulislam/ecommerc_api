from django.urls import path,include

from rest_framework.routers import DefaultRouter
from .views import CustomerRegistrationViewSet,GoogleLogin, FacebookLogin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'register', CustomerRegistrationViewSet, basename='register')
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("social/registration/", include("dj_rest_auth.registration.urls")),
    # social login endpoints
    path("social/google/", GoogleLogin.as_view(), name="google_login"),
    path("social/facebook/", FacebookLogin.as_view(), name="fb_login"),
]
