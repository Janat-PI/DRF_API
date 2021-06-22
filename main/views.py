import django_filters.rest_framework
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view
from .filters import ProductFilter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django_filters import rest_framework as filters
from  rest_framework.permissions import IsAuthenticated

# 1) Список товаров, доступен всем пользователям
# @api_view(['GET'])
# def products_list(request):
#     queryset = Product.objects.all()
#     filtered_qs = ProductFilter(request.GET, queryset=queryset)
#     print(queryset)
#     serializer = ProductListSerializer(filtered_qs.qs, many=True)
#     serializer_queryset = serializer.data
#     print(serializer_queryset)
#     return Response(data=serializer_queryset, status=status.HTTP_200_OK)


# class ProductsListView(APIView):
#     def get(self, request):
#         queryset = Product.objects.all()
#         filtered_qs = ProductFilter(request.GET, queryset=queryset)
#         print(queryset)
#         serializer = ProductListSerializer(filtered_qs.qs, many=True)
#         serializer_queryset = serializer.data
#         print(serializer_queryset)
#         return Response(data=serializer_queryset, status=status.HTTP_200_OK)


# 2) Детали товаров, доступны всем
class ProductsListView(ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filterset_class = ProductFilter


# 2) Детали товаров, доступны всем
class ProductDetailsView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

# 3) Создание товаров, редактировние, удаление доступно только админам
# class CreateProductView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer
#     permission_classes = [IsAdminUser]

# 3) Создание товаров, редактировние, удаление доступно только админам
# class UpdateProductView(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer
#     permission_classes = [IsAdminUser]

# 3) Создание товаров, редактировние, удаление доступно только админам
# class DeleteProductView(DestoryAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer
#     permission_classes = [IsAdminUser]


# 4) Создание отзывов, досткпно только залогиненым пользователям
class CreateReview(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}




# 5) Просмотр отзывов (внутри делталей продукта) длступна всем
# 6) Редактирование и удаление отзыва может делать только автор
# 7) Заказ может создть любой залогиненый пользватель
# 8) Список заказов пользоватеь видит только свои заказы, админы видят все
# 9) Редактировать заказы может только админ

