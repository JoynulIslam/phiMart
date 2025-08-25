from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category , Review,ProductImage
from product.serializer import ProductSerializer, CategorySerializer, ReviewSerializer,ProductImageSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from product.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly , FullDjangoModelPermission
from rest_framework.permissions import DjangoModelPermissions , DjangoModelPermissionsOrAnonReadOnly
from rest_framework.exceptions import PermissionDenied
from product.permissions import IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class ProductViewSet(ModelViewSet):
    """
     API endpoint for managing products in the e-commerce store
      - Allowed authenticated admin to create, update, delete product
      - Allowed users to browes and filter product
      - Searching by name, description, category name
    """   
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description' , 'category__name']
    ordering_fields = ['price']
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     return Product.objects.prefetch_related('images').all()

    @swagger_auto_schema(
    operation_summary="Retrieve a list of product",
    manual_parameters=[
        openapi.Parameter(
            "price__gt",
            openapi.IN_QUERY,
            description="Minimum price filter",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            "price__lt",
            openapi.IN_QUERY,
            description="Maximum price filter",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            "category_id",
            openapi.IN_QUERY,
            description="Category ID filter",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "search",
            openapi.IN_QUERY,
            description="Search by name, description, or category name",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "ordering",
            openapi.IN_QUERY,
            description="Order by price (use 'price' or '-price')",
            type=openapi.TYPE_STRING,
        ),
    ]
)



    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({"message" : "Product with stock more than 10 could not be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id = self.kwargs.get('product_pk'))
    

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
             raise PermissionDenied("Authentication required to post a review.")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
          

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return {'product_id': self.kwargs.get('product_pk')}


@api_view(['GET','POST'])
def view_product(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many = True )
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data = request.data) # Deserializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many = True )
        return Response(serializer.data)
    def post(self, request):
         serializer = ProductSerializer(data = request.data) # Deserializer
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def delete(self, request, id):
        product = get_object_or_404(Product, pk = id)
        if product.stock > 10:
            return Response({"message" : "Product with stock more than 10 could not be delete"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




@api_view(['GET','PUT','DELETE'])
def view_specific_product(request, id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk = id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    if request.method == 'PUT':
        product = get_object_or_404(Product, pk = id)
        serializer = ProductSerializer(product,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk = id)
        copy_of_product = product
        product.delete()
        serializer = ProductSerializer(copy_of_product)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
    

class ViewSpecificProduct(APIView):
    def get(self, request ,id):
        product = get_object_or_404(Product, pk = id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
         product = get_object_or_404(Product, pk = id)
         serializer = ProductSerializer(product,data = request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk = id)
        copy_of_product = product
        product.delete()
        serializer = ProductSerializer(copy_of_product)
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
    


@api_view()
def view_categories(request):
    categories = Category.objects.annotate(product_count=Count('products')).all()
    serializers = CategorySerializer(categories,many = True)
    return Response(serializers.data)

class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer


class ViewCategories(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('products')).all()
        serializers = CategorySerializer(categories,many = True)
        return Response(serializers.data)
    
    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)

@api_view()
def view_specific_categories(request, pk):
    category = get_object_or_404(Category.objects.annotate(product_count=Count('products')), pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

class ViewSpecificCategory(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')), pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')), pk=pk)
        serializer = CategorySerializer(category, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
         category = get_object_or_404(Category.objects.annotate(product_count=Count('products')), pk=pk)
         category.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
