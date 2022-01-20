from rest_framework import serializers
from .models import Category
from .models import Tag
from .models import Product
from .models import Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'is_active']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'value']


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField
    reviews = serializers.SerializerMethodField

    class Meta:
        model = Product
        fields = ['id', 'title', 'tags', 'price', 'category', 'description']


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews']

    def get_reviews(self, product):
        rate = Review.objects.filter(product=product, value__gt=2)
        data = ReviewSerializer(rate, many=True).data
        return data


class ProductTagSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_tags(self, product):
        return TagSerializer(product.tags.filter(is_active=True), many=True).data


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'tags', 'price', 'category', 'description']


class TagCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_active = serializers.BooleanField()

    def validate_name(self, name):
        tags = Tag.objects.filter(name = name)
        if tags:
            raise ValidationError("Tag already existed")
        return name

class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=25)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField
    tags = serializers.ListField(child=serializers.IntegerField())
    created_tags = serializers.ListField(child=TagCreateSerializer())

    def validate(self, attrs):
        title = attrs['title']
        products = Product.objects.filter(title=title)
        if products:
            raise ValidationError('This title of product already existed')
        return products
