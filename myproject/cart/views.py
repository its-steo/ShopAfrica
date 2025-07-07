from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from decimal import Decimal

from products.models import Product
from .models import Cart as CartModel, CartItem, SavedItem
from checkout.models import Order, OrderItem


# --------------------------
# Utility: Get Cart (Session or User)
# --------------------------
def get_cart_for_user(request):
    if request.user.is_authenticated:
        cart, _ = CartModel.objects.get_or_create(user=request.user, is_active=True)
    else:
        session_key = request.session.get("cart_session_key")
        if not session_key:
            session_key = get_random_string(32)
            request.session["cart_session_key"] = session_key
        cart, _ = CartModel.objects.get_or_create(session_key=session_key, is_active=True)
    return cart


# --------------------------
# View: Add to Cart
# --------------------------
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    selected_image_url = request.POST.get('selected_image_url')

    product = get_object_or_404(Product, id=product_id)

    # Check stock
    if product.quantity < quantity:
        return JsonResponse({
            'status': 'error',
            'message': f'Only {product.quantity} left in stock.'
        }, status=400)

    cart = get_cart_for_user(request)

    # Check if product already exists in cart
    if CartItem.objects.filter(cart=cart, product=product).exists():
        return JsonResponse({
            'status': 'exists',
            'message': 'Product already in cart.'
        })

    # Add new item
    CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=quantity,
        selected_image_url=selected_image_url
    )

    # Reduce stock
    product.quantity -= quantity
    product.save()

    # Recalculate cart count
    cart_count = CartItem.objects.filter(cart=cart).aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'status': 'success',
        'message': f'{product.name} added to cart.',
        'cart_count': cart_count,
        'available_quantity': product.quantity
    })


# --------------------------
# View: Cart Detail Page
# --------------------------
def cart_detail(request):
    cart = get_cart_for_user(request)
    items = CartItem.objects.filter(cart=cart)
    coupon_code = request.session.get('coupon_code', '')
    subtotal = 0
    cart_count = 0
    today = datetime.today()
    delivery_range = f"{(today + timedelta(days=2)).strftime('%b %d')} – {(today + timedelta(days=5)).strftime('%b %d')}"
   

     # If the cart is now empty, clear the coupon
    if not items and 'coupon_code' in request.session:
        del request.session['coupon_code']
        request.session.modified = True
        
    discounted_items = []
    for item in items:
        product = item.product
        quantity = item.quantity
        original_price = float(product.price)
        price = float(product.get_discounted_price(coupon_code))
        total = price * quantity
        subtotal += total
        cart_count += quantity

        discounted_items.append({
            'product': product,
            'quantity': quantity,
            'original_price': original_price,
            'final_price': price,
            'total': total,
            'coupon_applied': coupon_code == product.coupon_code,
            'estimated_delivery': delivery_range,
            'selected_image_url': item.selected_image_url,
        })

    delivery_fee = 300 if request.session.get('delivery_method', 'standard') == 'standard' else 600
    discount = request.session.get('coupon_discount', 0)
    total_price = subtotal

    saved_items = []
    if request.user.is_authenticated:
        saved_items = SavedItem.objects.filter(user=request.user)

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': discounted_items,
        'cart_count': cart_count,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total_price': total_price,
        'coupon_code': coupon_code,
        'saved_items': saved_items,
    })


# --------------------------
# View: Apply Coupon
# --------------------------
@csrf_exempt
@require_POST
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    cart = get_cart_for_user(request)
    items = CartItem.objects.filter(cart=cart)
    total_discount = 0

    for item in items:
        product = item.product
        if product.coupon_code == coupon_code:
            discount_percent = product.discount_percentage or 0
            total_discount += (Decimal(str(product.price)) * item.quantity) * (discount_percent / Decimal('100'))

    request.session['coupon_code'] = coupon_code
    request.session['coupon_discount'] = round(float(total_discount), 2)
    request.session.modified = True

    messages.success(request, f"Coupon '{coupon_code}' applied successfully.")
    return redirect('cart:cart_detail')


# --------------------------
# View: Remove from Cart
# --------------------------
@require_POST
def remove_from_cart(request, product_id):
    cart = get_cart_for_user(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        quantity = cart_item.quantity
        cart_item.delete()
        product.quantity += quantity
        product.save()
        messages.success(request, f"{product.name} removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, f"{product.name} not found in cart.")

    return redirect('cart:cart_detail')


# --------------------------
# View: Update Quantity
# --------------------------
@require_POST
def update_cart_quantity(request, product_id, action):
    cart = get_cart_for_user(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        item = CartItem.objects.get(cart=cart, product=product)
        if action == 'increase':
            if product.quantity < 1:
                messages.error(request, f"No more {product.name} in stock.")
            else:
                item.quantity += 1
                product.quantity -= 1
                item.save()
                product.save()
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                product.quantity += 1
                item.save()
                product.save()
            else:
                item.delete()
                product.quantity += 1
                product.save()
    except CartItem.DoesNotExist:
        messages.error(request, f"{product.name} not found in cart.")
    return redirect('cart:cart_detail')


# --------------------------
# View: Save for Later
# --------------------------
@login_required
def save_for_later(request, product_id):
    if request.method == "POST":
        cart = CartModel.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return redirect('cart:cart_detail')

        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        SavedItem.objects.get_or_create(
            user=request.user,
            product=item.product,
            variety=None
        )
        item.delete()
    return redirect('cart:cart_detail')


# --------------------------
# View: Move to Cart
# --------------------------
@login_required
def move_to_cart(request, item_id):
    if request.method == "POST":
        saved_item = get_object_or_404(SavedItem, id=item_id, user=request.user)
        cart, _ = CartModel.objects.get_or_create(user=request.user, is_active=True)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=saved_item.product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        saved_item.delete()
    return redirect('cart:cart_detail')


# --------------------------
# Extra Utility Views
# --------------------------
def quick_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/quick_view_partial.html', {'product': product})


def clear_cart(request):
    cart = get_cart_for_user(request)
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        product = item.product
        product.quantity += item.quantity
        product.save()
    cart_items.delete()
    cart.is_active = False
    cart.save()
    messages.success(request, "Cart cleared.")
    return redirect('cart:cart_detail')


def test_session(request):
    request.session['test'] = 'Session OK'
    return HttpResponse(f"Session: {request.session.get('test')}")
