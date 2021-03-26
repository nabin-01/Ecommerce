from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('my-account/', my_account, name='my_account'),
    path('product-detail/', product_detail, name='product_detail'),
    path('product-list/', product_list, name='product_list'),
    path('wishlist/', wishlist, name='wishlist'),
]
