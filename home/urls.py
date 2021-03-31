from django.urls import path
from .views import *
app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product-list/', ListView.as_view(), name='product-list'),
    path('products/<slug>', ItemDetailView.as_view(), name='products'),
    # path('cart/', 'cart.html', name='cart'),
    # path('checkout/', 'checkout.html', name='checkout'),
    # path('my-account/', 'my-account.html', name='my-account'),
    # path('wishlist/', 'wishlist.html', name='wishlist'),
    # path('login/', 'login.html', name='login'),
    # path('contact/', 'contact.html', name='contact'),
]
