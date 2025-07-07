from django.shortcuts import get_object_or_404, render
from .models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from django.core.mail import send_mail
from django.conf import settings


def products_view(request):
    all_products = Product.objects.all()
    return render(request, 'products/products.html', {'products': all_products})

def quick_view_partial(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/quick_view_partial.html', {'product': product})

@csrf_exempt  # Remove this if using CSRF token in form
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already subscribed.'})
            Subscriber.objects.create(email=email)
            return JsonResponse({'status': 'success', 'message': 'Subscribed successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Email is required.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

# products/views.py

from django.shortcuts import render
from .models import Product
from django.db.models import Q

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'products.html', {
        'products': products,
         
    })



