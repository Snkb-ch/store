from django.urls import path, include
from rest_framework_nested import routers

from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'cart', CartViewSet, basename='cart')









products_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
products_router.register(r'reviews', ReviewViewSet, basename='product-reviews')







urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(products_router.urls)),
    path('reviews/', UserReviews.as_view(), name='user-reviews'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/<int:product_id>/', WishlistView.as_view(), name='wishlist-manage'),




]