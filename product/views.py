from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = (
        Category.objects.filter(parent__isnull=True, is_active=True)
        .select_related("parent")
        .prefetch_related("children")
    )
    serializer_class = CategorySerializer
    lookup_field = "slug"
    http_method_names = [
        "get",
        "post",
    ]

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs["slug"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    http_method_names = [
        "get",
        "post",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category", None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
