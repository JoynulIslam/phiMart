from django.shortcuts import render
from order.serializers import CartSerializer , CartItemSerializer ,AddCartItemSerializer, UpdateCartItemSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer,EmptySerializer
from rest_framework.viewsets import GenericViewSet , ModelViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin,DestroyModelMixin
from order.models import Cart ,CartItem,Order,OrderItem
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CartViewSet(CreateModelMixin ,DestroyModelMixin ,GenericViewSet,RetrieveModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Cart.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "You already have a cart."})
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        if not self.request.user.is_authenticated:
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()

        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)


class CartItemsViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        return {'cart_id' : self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','delete','patch','head','options']
    
    @action(detail=True, methods = ['post'])
    def cancel(self, request ,pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order , user = request.user)
        return Response({"status" : "Order Canceled"})
    
    @action(detail=True, methods = ['patch'])
    def update_status(self, request, pk = None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(
            order, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status' : f"Order status updated to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ['destroy' , 'update_status']:
            return [IsAdminUser()]        
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'update_status':
            return UpdateOrderSerializer
        return OrderSerializer    
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id' : self.request.user.id , 'user' : self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if not self.request.user.is_authenticated:
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)


