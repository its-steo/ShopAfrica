from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('quick-view/<int:pk>/', views.quick_view, name='quick_view'),
    path('save/<int:product_id>/', views.save_for_later, name='save_for_later'),
    path('move-to-cart/<int:item_id>/', views.move_to_cart, name='move_to_cart'),
     path('save-for-later/<int:product_id>/', views.save_for_later, name='save_for_later'),
]
