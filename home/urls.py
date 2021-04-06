from django.urls import path
from .views import *
app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('product-list/', ListView.as_view(), name='product-list'),
    path('products/<slug>', ItemDetailView.as_view(), name='products'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('search/', SearchView.as_view(), name='search'),
    path('contact/', contact, name='contact'),
    path('account/', signup, name='account'),
]
