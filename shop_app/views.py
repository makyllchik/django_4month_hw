from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, TagSerializer, ProductSerializer, ReviewSerializer
from .serializers import ProductReviewSerializer, ProductTagSerializer, ProductDetailSerializer
from .models import Category, Tag, Product, Review
from rest_framework import status
from .serializers import ProductCreateSerializer


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
def review_detail_view(request, id):
    category = Review.objects.get(id=id)
    data = ReviewSerializer(category).data
    return Response(data=data)


@api_view(['GET'])
def product_list_view(request):
    category = Product.objects.all()
    data = ProductSerializer(category, many=True).data
    return Response(data=data)


@api_view(['GET', 'DELETE', 'PUT'])
def product_detail_view(request, id):
    try:
        category = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Product ЖОК'})

    if request.method == 'GET':
        data = ProductDetailSerializer(category, many=False).data
        return Response(data=data)

    elif request.method == 'DELETE':
        category.delete()
        return Response(data={'message': 'Product successfully -'})

    elif request.method == 'PUT':
        serializer = ProductCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        print('serializer.initial_data', serializer.initial_data)

        category.title = serializer.initial_data['title']
        category.description = serializer.initial_data.get('description', '')
        category.price = serializer.initial_data['price']
        tags = serializer.initial_data['tags']
        category.tags.set(tags)
        category.save()
        data = ProductDetailSerializer(category).data
        Response(data=data)
    return Response(data=ProductDetailSerializer(category).data,
                    status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def product_review_view(request):
    category = Product.objects.all()
    data = ProductReviewSerializer(category, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_tag_view(request):
    category = Product.objects.all()
    data = ProductTagSerializer(category, many=True).data
    return Response(data=data)
