from rest_framework import serializers
from .models import Product, Category, Order, Customer, Cart

from rest_framework import serializers
from .models import *
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'comment', 'rating', 'customer', 'date_created']
        read_only_fields = ['id', 'date_created', 'customer']

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['comment', 'rating']




class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = []

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'customer', 'date_ordered', 'transaction_id']



class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    product_id = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['id', 'product_id', 'quantity', 'created_at']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Продукт с указанным ID не существует.")
        return value


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'customer']
        read_only_fields = ['id', 'customer']
