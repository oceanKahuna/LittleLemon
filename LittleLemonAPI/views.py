from django.shortcuts import render
from rest_framework import generics, permissions
from .models import * 
from .serializers import * 
from django.contrib.auth.models import Group
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


# Create your views here.

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for admins or request is read only
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
    
class IsAdminUser(permissions.BasePermission):
    """
    Custom permission for admins.
    """
    def has_permission(self, request, view):
        return request.user.is_staff
    
class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission so that only managers can edit
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Manager').exists()
    
class IsDeliveryCrewOrReadOnly(permissions.BasePermission):
    """Permission for only delivery crew to edit"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='DeliveryCrew').exists()

class MenuItemFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__title",lookup_expr="iexact")

    class Meta:
        model = MenuItem
        fields = ['category']
        
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MenuItemFilter
    ordering_fields = ['title','price']
    search_fields = ['title','price']
    

class MenuItemView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly, IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = MenuItemFilter
    ordering_fields = ['title','price']
    search_fields = ['title','price']

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() and not request.user.is_staff:
            allowed_fields = {'featured'}
            for field in request.data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError(f'Managers are not allowed to update the {field} field')
        return super(MenuItemView, self).update(request, *args, **kwargs)

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permissions_classes = [IsAdminOrReadOnly]

class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

class UserView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    ALLOWED_GROUPS_FOR_MANAGERS = ['DeliveryCrew','Customer']

    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() and not request.user.is_staff:
            allowed_fields = {'groups'}
            for field in request.data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError(f'Managers are not allowed to update the {field} field')
                
            groups = request.data.get('groups',[])
            incoming_group_names = [Group.objects.get(id=group_id).name for group_id in groups]
            
            for group_name in incoming_group_names:
                if group_name not in ALLOWED_GROUPS_FOR_MANAGERS:
                    raise serializers.ValidationError(f'Managers cannot assign users to {groups} group')
        return super(UserView, self).update(request, *args, **kwargs)

class GroupsView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly, IsManagerOrReadOnly, IsDeliveryCrewOrReadOnly]

    def get_queryset(self):
        user = self.request.user 
        if user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(assigned_to=user)
        elif user.groups.filter(name='Customer').exists():
            return Order.objects.filter(user=user)
        return Order.objects.all()

class OrderView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly, IsManagerOrReadOnly, IsDeliveryCrewOrReadOnly]

    def get_queryset(self):
        user = self.request.user 
        if user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(assigned_to=user)
        elif user.groups.filter(name='Customer').exists():
            return Order.objects.filter(user=user)
        return Order.objects.all()
    
    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='DeliveryCrew').exists() and not request.user.is_staff:
            allowed_fields = {'status'}
            for field in request.data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError(f'Delivery Crew are not allowed to update the {field} field')

class CartsView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Customer').exists():
            return Cart.objects.filter(user=user)
        return Cart.objects.all()
           
class CartView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer 

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Customer').exists():
            return Cart.objects.filter(user=user)
        return Cart.objects.all()
    

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ConvertCartToOrderView(APIView):
    permission_classes = [IsAuthenticated]  # and any other permissions you may want

    def post(self, request):
        user = request.user

        # Get the cart items for the user
        cart_items = Cart.objects.filter(user=user)

        # Check if the cart is empty
        if not cart_items.exists():
            return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order
        total_price = sum(item.price for item in cart_items)
        order = Order.objects.create(user=user, total=total_price)

        # Create order items and clear the cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            cart_item.delete()  # remove item from cart

        return Response({"detail": "Order created successfully."}, status=status.HTTP_201_CREATED)


