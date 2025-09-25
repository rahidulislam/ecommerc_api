from rest_framework import viewsets, status
from rest_framework.response import Response


from .serializers import CategorySerializer
from .services import CategoryService
# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    serializer_class = CategorySerializer

    # queryset = Category.objects.all()
    def list(self, request):
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            is_active = is_active.lower() == "true"
        categories = CategoryService.list_categories(is_active=is_active)
        return Response(self.serializer_class(categories, many=True).data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                category = CategoryService.create_category(serializer.validated_data)
                return Response(
                    self.serializer_class(category).data, status=status.HTTP_201_CREATED
                )
            except ValueError as error:
                return Response(
                    {"error": str(error)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
