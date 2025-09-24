from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.conf import settings
from users.models import User
from users.serializers import CustomerSerializer


# Create your views here.
class CustomerRegistrationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = [
        "post",
        "head",
        "options",
    ]  # Limit to only POST method for registration

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"details": "User registered successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# project/social_views.py


# If using redirect URI flows in server-side, you may need client_id and secret in settings.
# For token exchange (frontend obtains access_token then posts to backend), the adapter + SocialLoginView is enough.

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # callback_url not required if using frontend token; include if doing server-side flow
    # callback_url = "http://localhost:8000/"

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    # callback_url = "http://localhost:8000/"
