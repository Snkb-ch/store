from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import Product, Category, Order, Cart, Wishlist
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsOwner, IsAdmin
from .serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_pk')
        request.data['product'] = product_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return Review.objects.filter(product_id=product_id)

    def get_serializer_class(self):
        if self.action == 'update':
            return ReviewUpdateSerializer
        return ReviewSerializer






class UserReviews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.filter(customer=request.user)
        return Response(ReviewSerializer(reviews, many=True).data)


class CreateCustomerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name=data['name'],
            email=data['email']
        )
        return Response(CustomerSerializer(customer).data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_400_BAD_REQUEST)


# cart
class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            quantity = serializer.validated_data.get('quantity', 1)
            cart, created = Cart.objects.get_or_create(customer=request.user, product=product)
            cart.quantity += quantity
            cart.save()

            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            # delete cart item
            cart = Cart.objects.filter(customer=request.user, product=product)
            if cart.exists():
                cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def decrease(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.filter(customer=request.user, product=product).first()
            if cart:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()
                else:
                    cart.delete()
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def increase(self, request, *args, **kwargs):


        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.filter(customer=request.user, product=product).first()
            if cart:
                cart.quantity += 1
                cart.save()
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_quantity(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            cart = Cart.objects.filter(customer=request.user, product=product).first()
            if cart:
                cart.quantity = serializer.validated_data.get('quantity')
                cart.save()
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def clear_cart(self, request, *args, **kwargs):
        Cart.objects.filter(customer=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class WishlistView(APIView):
    permission_classes = [IsOwner]


    def get(self, request):
        wishlist = Wishlist.objects.filter(customer=request.user)
        serializer = WishListSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            product= serializer.validated_data.get('product')

            wishlist, created = Wishlist.objects.get_or_create(customer=request.user, product=product)
            if not created:
                return Response({'error': 'Товар уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(WishListSerializer(wishlist).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')

        wishlist = Wishlist.objects.filter(customer=request.user, product_id=product_id)
        if wishlist.exists():
            wishlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Товар не найден в избранном'}, status=status.HTTP_400_BAD_REQUEST)



class OrderViewSet(viewsets.ModelViewSet):
    class OrderViewSet(viewsets.ModelViewSet):
        """
        A viewset for viewing and editing order instances.
        """
        serializer_class = OrderSerializer
        permission_classes = [IsAuthenticated, IsOwner]

        def get_permissions(self):
            if self.action == 'create':
                return [IsAuthenticated()]
            elif self.action in ['update', 'destroy']:
                return [IsAdmin()]
            return [IsOwner()]



        def get_queryset(self):
            # IsAdmin могут видеть все заказы, пользователи только свои
            if self.request.user.is_staff:
                return Order.objects.all()
            return Order.objects.filter(customer=self.request.user)

        @action(detail=False, methods=['get'], permission_classes=[IsOwner])
        def active(self, request):
            # Возвращает активные заказы пользователя
            orders = Order.objects.filter(customer=request.user, status__in=["Created", "Processing"])
            return Response(OrderSerializer(orders, many=True).data)


        @action(detail=True, methods=['patch'], permission_classes=[IsOwner])
        def cancel(self, request, pk=None):
            """
            Allows customers to cancel their order.
            """
            order = get_object_or_404(Order, pk=pk)

            if order.status not in ["Created", "Processing"]:
                return Response({"error": "Невозможно отменить выполненный или доставленный заказ."},
                                status=status.HTTP_400_BAD_REQUEST)

            order.status = "Cancelled"
            order.save()
            return Response({"message": "Заказ отменен."}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # create order from cart
        cart = Cart.objects.filter(customer=self.request.user)
        if not cart.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save(customer=self.request.user)
        for item in cart:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                quantity=item.quantity
            )
        cart.delete()
        return Response(CreateOrderSerializer(order).data)











