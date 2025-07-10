from django.urls import path
from . import views
from .views import test_email_view

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('test-email/', test_email_view, name='test_email'),
    path('track-order/<int:order_id>/', views.track_order_view, name='track_order'),
    path('order-cancel/<int:order_id>/', views.cancel_order_view, name='cancel_order'),
    path('continue-shopping/', views.clear_session_and_redirect, name='clear_session_and_redirect'),
    path('order-history/', views.order_history_view, name='order_history'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),

   

]

