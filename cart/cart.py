from products.models import Product
from .models import Cart as CartModel, CartItem
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.db.models import Sum
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self._get_cart_for_user()
        print(f"Initialized cart: {self.cart.id}, items: {self.cart.items.count()}")  # Debug

    def _get_cart_for_user(self):
        """Get or create a CartModel for the user or session."""
        if self.request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=self.request.user, is_active=True)
        else:
            session_key = self.session.get("cart_session_key")
            if not session_key:
                session_key = get_random_string(32)
                self.session["cart_session_key"] = session_key
                self.session.modified = True
            cart, _ = CartModel.objects.get_or_create(session_key=session_key, is_active=True)
        return cart

    def has(self, product):
        """Check if a product already exists in the cart."""
        exists = CartItem.objects.filter(cart=self.cart, product=product).exists()
        print(f"Check if product {product.id} in cart {self.cart.id}: {exists}")
        return exists

    def add(self, product, quantity=1, selected_image_url=None):
        """Add product to cart if not already added."""
        if self.has(product):
            print(f"Product {product.id} already in cart {self.cart.id}, not adding again.")
            return

        CartItem.objects.create(
            cart=self.cart,
            product=product,
            quantity=quantity,
            selected_image_url=selected_image_url
        )
        product.quantity -= quantity
        product.save()
        print(f"Added product {product.id} to cart {self.cart.id}, qty: {quantity}")

    def get_items(self):
        """Retrieve cart items with pricing and discounts."""
        items = []
        coupon_code = self.request.session.get('coupon_code', '')
        print(f"Processing cart items for cart {self.cart.id}, coupon: {coupon_code}")

        for cart_item in CartItem.objects.filter(cart=self.cart):
            product = cart_item.product
            quantity = cart_item.quantity
            original_price = float(product.price)
            price = cart_item.unit_price  # Use CartItem property
            total = cart_item.total_price  # Use CartItem property

            items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': total,
                'original_price': original_price,
                'coupon_applied': coupon_code == product.coupon_code,
                'selected_image_url': cart_item.selected_image_url,
                'estimated_delivery': self._get_estimated_delivery(),
            })
            print(f"Item {product.id}: qty={quantity}, price={price}, total={total}")

        print(f"Cart items processed: {len(items)} items")
        return items

    def __iter__(self):
        return iter(self.get_items())

    def get_subtotal_price(self):
        """Calculate subtotal of all items."""
        items = self.get_items()
        subtotal = sum(item['total'] for item in items) if items else 0
        print(f"Subtotal for cart {self.cart.id}: {subtotal}")
        return subtotal

    def get_delivery_fee(self):
        """Calculate delivery fee based on session delivery method."""
        method = self.request.session.get('delivery_method', 'standard')
        fee = 300 if method == 'standard' else 600 if method == 'express' else 0
        print(f"Delivery method: {method}, fee: {fee}")
        return fee

    def get_discount(self):
        """Calculate total discount for coupon code applied to all matching items."""
        coupon_code = self.request.session.get('coupon_code')
        if not coupon_code:
            return 0.0
    
        total_discount = Decimal('0.0')
        for item in CartItem.objects.filter(cart=self.cart):
            product = item.product
            if product.coupon_code == coupon_code and product.discount_percentage:
                unit_price = product.price  # Keep this as Decimal
                discount_per_item = (product.discount_percentage / Decimal('100')) * unit_price
                total_discount += discount_per_item * item.quantity
                print(f"Discount on product {product.name}: {discount_per_item} × {item.quantity} = {discount_per_item * item.quantity}")
    
        print(f"Total coupon discount: {total_discount}")
        return total_discount


    def get_total(self):
        """Get the total amount (subtotal + delivery - discount)."""
        subtotal = self.get_subtotal_price()
        delivery_fee = self.get_delivery_fee()
        total = subtotal + delivery_fee
        print(f"Total for cart {self.cart.id}: subtotal {subtotal} + delivery {delivery_fee} = {total}")
        return total

    def clear(self):
        """Clear cart and restore stock."""
        cart_items = CartItem.objects.filter(cart=self.cart)
        for item in cart_items:
            product = item.product
            product.quantity += item.quantity
            product.save()
        cart_items.delete()
        self.cart.is_active = False
        self.cart.save()
        print(f"Cleared cart {self.cart.id}")

    def _get_estimated_delivery(self):
        """Calculate estimated delivery date."""
        method = self.request.session.get('delivery_method', 'standard')
        days = 5 if method == 'standard' else 2
        delivery_date = timezone.now() + timedelta(days=days)
        formatted_date = delivery_date.strftime('%A, %d %B')
        print(f"Estimated delivery: {formatted_date}")
        return formatted_date

    def count(self):
        """Return total quantity of items in the cart."""
        total_count = CartItem.objects.filter(cart=self.cart).aggregate(total=Sum('quantity'))['total'] or 0
        print(f"Cart count for cart {self.cart.id}: {total_count}")
        return total_count
    
