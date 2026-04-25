from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import CartItem
from apps.cart.serializers import CartItemSerializer, CartSerializer
from apps.cart.services import add_product_to_cart, get_or_create_cart


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartItemListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = add_product_to_cart(
            cart=cart,
            product=serializer.validated_data["product"],
            quantity=serializer.validated_data["quantity"],
            milk_type=serializer.validated_data.get("milk_type")
            or CartItem.MilkType.REGULAR,
        )
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch", "delete"]

    def get_queryset(self):
        cart = get_or_create_cart(self.request.user)
        return CartItem.objects.filter(cart=cart)


class CartClearView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
