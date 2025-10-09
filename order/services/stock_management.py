from django.db import transaction


class StockManager:
    @staticmethod
    @transaction.atomic
    def deduct_product_stock(product, quantity):
        product.stock -= quantity
        product.save()
