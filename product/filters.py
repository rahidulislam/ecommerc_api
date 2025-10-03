from django_filters import rest_framework as filters
from product.models import Product

class ProductFilter(filters.FilterSet):
    category=filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    in_stock = filters.BooleanFilter(method='filter_in_stock')
    class Meta:
        model = Product
        fields = ['category', 'in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value is True:
            return queryset.filter(stock__gt=0)
        elif value is False:
            return queryset.filter(stock__lte=0)
        return queryset
