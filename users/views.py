from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
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
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
