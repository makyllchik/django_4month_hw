from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, TagSerializer, ProductSerializer, ReviewSerializer
from .models import Category, Tag, Product, Review


@api_view(['GET'])
def category_list_view(request):
    category = Category.objects.all()
    data = CategorySerializer(category, many=True).data
    return Response(data=data)


@api_view(['GET'])
def tag_list_view(request):
    category = Tag.objects.all()
    data = TagSerializer(category, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_list_view(request, id):
    category = Product.objects.get(id=id)
    data = ProductSerializer(category).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_view(request, id):
    category = Review.objects.get(id=id)
    data = ReviewSerializer(category).data
    return Response(data=data)
