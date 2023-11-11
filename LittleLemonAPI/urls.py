from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import * 
from django.urls import path, include

urlpatterns = [
    path('menuitems',MenuItemsView.as_view(), name='menu-items'),
    path('menuitem/<int:pk>',MenuItemView.as_view(), name = 'menu_item'),
    path('categories',CategoriesView.as_view(), name='categories'),
    path('category/<int:pk>',CategoryView.as_view(), name='category'),
    path('carts/',CartsView.as_view(),name='carts'),
    path('cart/<int:pk>',CartView.as_view(), name = 'cart'),
    path('api-token-auth',obtain_auth_token,name='api-token-auth'),
    path('user/<int:pk>',UserView.as_view(),name='user'),
    path('users',UsersView.as_view(),name='users'),
    path('groups',GroupsView.as_view(),name='groups'),
    path('orders', OrdersView.as_view(), name='orders'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh_view'),
    path('order_cart/',ConvertCartToOrderView.as_view(), name='order_cart')
]

