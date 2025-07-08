"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from products import views as products_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', products_views.products_view, name='products'),
    path('cart/', include('cart.urls')),
    path('home/', accounts_views.home, name='home'),
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.login_view, name='login'),
    path('products/quick-view/<int:product_id>/', products_views.quick_view_partial, name='quick_view_partial'),
    path('subscribe/', products_views.subscribe_newsletter, name='subscribe_newsletter'),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    #path('accounts/', include('allauth.urls')), 
    #path('', include('accounts.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

