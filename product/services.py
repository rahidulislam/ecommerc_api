from django.core.exceptions import ObjectDoesNotExist
from .models import Category


class CategoryService:
    @staticmethod
    def list_categories(is_active=None):
        queryset = Category.objects.filter(parent__isnull=True).select_related("parent")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        return queryset.order_by("name")

    @staticmethod
    def get_category_by_slug(slug):
        try:
            return Category.objects.get(slug=slug, is_active=True)
        except Category.DoesNotExist:
            return ObjectDoesNotExist(
                f"Category with slug '{slug}' not found or inactive."
            )

    @staticmethod
    def create_category(data):
        parent = data.get("parent")
        print(parent)
        if parent:
            try:
                parent_instance = Category.objects.get(id=parent.id, is_active=True)
                data["parent"] = parent_instance
            except Category.DoesNotExist as error:
                raise ValueError("Invalid parent category") from error
        return Category.objects.create(**data)
