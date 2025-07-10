from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import timedelta

from .models import Order, OrderItem, Payment
from .forms import PaymentForm
from cart.cart import Cart
from cart.models import Cart as CartModel, CartItem
from products.models import Product


def checkout_view(request):
    cart = Cart(request)
    items = list(cart)
    subtotal = Decimal(str(cart.get_subtotal_price()))
    discount_amount = Decimal(str(cart.get_discount()))
    coupon_code = request.session.get('coupon_code')
    delivery_method = request.session.get('delivery_method', 'standard')

    delivery_fee = {
        'standard': Decimal('300.00'),
        'express': Decimal('600.00'),
        'cash_on_delivery': Decimal('0.00')
    }.get(delivery_method, Decimal('0.00'))

    total = subtotal - discount_amount + delivery_fee

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        delivery_method = request.POST.get('delivery_method')
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes')

        request.session['delivery_method'] = delivery_method
        request.session.modified = True

        delivery_fee = {
            'standard': Decimal('300.00'),
            'express': Decimal('600.00'),
            'cash_on_delivery': Decimal('0.00')
        }.get(delivery_method, Decimal('0.00'))

        total = subtotal - discount_amount + delivery_fee
        estimated_delivery = timezone.now().date() + timedelta(days=5 if delivery_method == 'standard' else 2)

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            delivery_method=delivery_method,
            payment_method=payment_method,
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            total_amount=total,
            estimated_delivery=estimated_delivery,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_time=item['price'],
            )

        cart.clear()

        html_message = render_to_string("checkout/order_success.html", {
            "order": order,
            "items": order.items.all(),
            "subtotal": subtotal,
            "discount": discount_amount,
            "delivery_fee": delivery_fee,
            "total_price": total,
            "estimated_delivery": estimated_delivery,
        })

        send_mail(
            subject="Order Confirmation - ShopAfrica",
            message="Your order has been received successfully.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        messages.success(request, "Order placed successfully.")
        return redirect('checkout:order_success', order_id=order.id)

    estimated_delivery = timezone.now().date() + timedelta(days=5 if delivery_method == 'standard' else 2)

    return render(request, 'checkout/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'delivery_fee': delivery_fee,
        'total_price': total,
        'estimated_delivery': estimated_delivery,
        'coupon_code': coupon_code,
        'cart_count': len(items),
        'delivery_method': delivery_method,
        'user_profile': {
            'full_name': request.user.get_full_name() if request.user.is_authenticated else '',
            'email': request.user.email if request.user.is_authenticated else '',
            'phone': '',
            'city': '',
            'address': '',
            'notes': '',
        },
    })


def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    subtotal = sum([item.price_at_time * item.quantity for item in items])
    discount = order.discount_amount or Decimal('0.00')
    delivery_fee = {
        'standard': Decimal('300.00'),
        'express': Decimal('600.00'),
    }.get(order.delivery_method, Decimal('0.00'))
    total_price = subtotal - discount + delivery_fee

    return render(request, 'checkout/order_success.html', {
        'order': order,
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'delivery_fee': delivery_fee,
        'total_price': total_price,
    })


@csrf_exempt
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount_paid = request.POST.get('amount_paid')
        screenshot = None

        if payment_method in ['mpesa', 'paypal', 'bank_transfer', 'crypto']:
            screenshot = request.FILES.get(f'{payment_method}_screenshot')

        if payment_method == 'mpesa':
            if not amount_paid:
                return JsonResponse({'success': False, 'message': 'Please enter the amount paid.'})

            try:
                amount_paid = float(amount_paid)
                expected = float(order.total_amount)
                if round(amount_paid, 2) != round(expected, 2):
                    return JsonResponse({'success': False, 'message': 'Payment declined. Amount does not match.'})
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Invalid amount format.'})

        Payment.objects.create(
            order=order,
            method=payment_method,
            screenshot=screenshot
        )

        if order.order_status != 'processing':
            order.order_status = 'processing'
            order.save()

            try:
                send_mail(
                    subject=f"Payment Received for Order #{order.id}",
                    message=f"Dear {order.full_name},\n\nWe have received your payment for Order #{order.id}.\n\nYour order is now being processed.\n\nThank you for shopping with us!\n\n-- ShopEase Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")

        return JsonResponse({'success': True, 'message': 'Payment successful!'})

    return render(request, 'checkout/payment_popup.html', {
        'order': order,
        'expected_amount': float(order.total_amount),
    })


def order_successful(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.order_status != "processing":
        order.order_status = "processing"
        order.save()

        try:
            send_mail(
                subject=f"Order #{order.id} is now Processing",
                message=f"Dear {order.full_name},\n\nWe have received your payment for Order #{order.id}.\n\nYour order is now being processed and will be shipped soon.\n\nThank you for shopping with us!\n\n-- ShopEase Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
            )
        except Exception as e:
            print(f"Error sending email: {e}")

    button_text = "Track Order" if order.order_status == "processing" else "Make Payment"

    return render(request, 'checkout/order_successful.html', {
        'order': order,
        'subtotal': order.total_amount,
        'discount': order.discount_amount,
        'delivery_fee': 0,
        'total_price': order.total_amount,
        'button_text': button_text,
    })


def track_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order_steps = ['pending', 'processing', 'shipping', 'delivered']
    current_index = order_steps.index(order.order_status) if order.order_status in order_steps else 0

    steps_data = []
    for idx, step in enumerate(order_steps):
        steps_data.append({
            'name': step.capitalize(),
            'status': step,
            'is_active': idx <= current_index,
            'is_current': idx == current_index,
        })

    return render(request, 'checkout/track_order.html', {
        'order': order,
        'steps': steps_data,
    })


def test_email_view(request):
    send_mail(
        subject='Test Email from ShopAfrica',
        message='This is a test email.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['receiver@example.com'],
        fail_silently=False,
    )
    return HttpResponse("Test email sent.")


@csrf_protect
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.order_status in ['pending']:
        order.order_status = 'cancelled'
        order.save()

        try:
            send_mail(
                subject=f"Order #{order.id} Cancelled",
                message=f"Dear {order.full_name},\n\nYour order #{order.id} has been cancelled as requested.\n\nIf this was a mistake or you need help, contact our support team.\n\n-- ShopEase Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Email error:", e)

        messages.success(request, "Your order has been cancelled successfully.")

    return redirect('checkout:order_success', order_id=order.id)


def clear_session_and_redirect(request):
    request.session.pop('cart', None)
    request.session.pop('coupon', None)
    request.session.modified = True
    return redirect('products')


@login_required
def order_history_view(request):
    orders_qs = Order.objects.filter(user=request.user).order_by('-created_at')
    for order in orders_qs:
        order.total = order.get_total_cost() if hasattr(order, 'get_total_cost') else order.total_amount

    paginator = Paginator(orders_qs, 5)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    return render(request, 'checkout/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    return render(request, 'checkout/order_detail.html', {
        'order': order,
        'items': items,
    })
