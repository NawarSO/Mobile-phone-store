from rest_framework import serializers
from .models import User, Mobile, Cart, CartItem, Order, PhoneSpecs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    mobile = MobileSerializer()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'mobile', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set')
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total']

    def get_total(self, obj):
        return obj.calculate_total()

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = '__all__'
class PhoneSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneSpecs
        fields = ['id', 'brand', 'model', 'ram', 'storage', 'screen_size', 'condition', 'estimated_price']
        read_only_fields = ['id', 'estimated_price']