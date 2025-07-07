from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_view, name='product_list'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('', views.product_list, name='products')
]