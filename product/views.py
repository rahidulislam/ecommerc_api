from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from product.models import Category, Product
from product.serializers import CategorySerializerList, CategorySerializerRetrive, CategorySerializerCreate, ProductSerializer
from product.filters import ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = (
        Category.objects.filter(parent__isnull=True, is_active=True)
        .select_related("parent")
        .prefetch_related("children")
    )
    lookup_field = "slug"
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete"
    ]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ["create", "partial_update"]:
            self.serializer_class = CategorySerializerCreate
        elif self.action == "list":
            self.serializer_class = CategorySerializerList
        elif self.action == "retrieve":
            self.serializer_class = CategorySerializerRetrive
        return super().get_serializer_class()


    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs["slug"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": f"{instance} category is deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    lookup_field = "slug"
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete"
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category", None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"detail": f"{instance} product is deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
