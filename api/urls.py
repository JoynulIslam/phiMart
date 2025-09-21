from django.urls import path,include

from product.views import ProductViewSet, CategoryViewSet,ReviewViewSet,ProductImageViewSet
from order.views import CartViewSet , CartItemsViewSet,OrderViewSet,initiate_payment
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products',ProductViewSet ,basename = 'products')
router.register('categories', CategoryViewSet)
router.register('carts' , CartViewSet , basename= 'carts')
router.register('orders' , OrderViewSet , basename= 'orders')

product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',ReviewViewSet,basename='product-review')

cart_router = routers.NestedDefaultRouter(router,'carts',lookup ='cart')
cart_router.register('items',CartItemsViewSet,basename='cart-item')

product_router.register('images' , ProductImageViewSet , basename='product-image')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(product_router.urls)),
    path('',include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/', initiate_payment,name="initiate_payment"),
    # extra
  
]
