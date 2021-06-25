from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'image')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def get_rating(self, instance):
        total_rating = sum(instance.reviews.values_list('rating', flat=True))
        reviews_count = instance.reviews.count()
        rating = total_rating/reviews_count if reviews_count > 0 else 0
        return round(rating, 1)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializers(instance.reviews.all(), many=True).data
        representation['rating'] = self.get_rating(instance)
        return representation


class ReviewAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.first_name and not instance.last_name:
            representation['full_name'] = 'Аноинмный пользователь'
        return representation


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('id', 'author')

    def validate_product(self, product):
        request = self.context.get('request')
        if product.reviews.filter(author=request.user).exists():
            raise serializers.ValidationError('yor are not add ')
        return product

    def validate_rating(self, rating):
        if not rating in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = ReviewAuthorSerializer(instance.author).data
        return rep


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', 'notes')

    def create(self, validated_data):
        total_sum = 0
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        validated_data['status'] = 'new'
        validated_data['total_sum'] = 0
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for prod in products:
            total_sum += prod['product'].price * prod['quantity']
            OrderItems.objects.create(order=order, **prod)
        order.total_sum = total_sum
        order.save()
        return order
