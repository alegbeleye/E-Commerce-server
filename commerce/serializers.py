from commerce.models import Customer, Product
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "email", "first_name", "last_name", "hashed_password", "country")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "original_price", "product_info", "product_image_url", "current_price", "price_percentage_cut", "amount_available_in_stock", "rating")