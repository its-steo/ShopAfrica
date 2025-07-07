document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
      const productId = button.dataset.productId;
      const quantity = 1;

      // Get selected image from closest image wrapper (fallback to blank)
      const selectedImage =
        button.closest('.image-wrapper')?.querySelector('img')?.src || '';

      fetch('/cart/add-to-cart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCSRFToken()
        },
        body: `product_id=${productId}&quantity=${quantity}&selected_image_url=${encodeURIComponent(selectedImage)}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          updateCartCounter(data.cart_count);
          showToast("Product added to cart", "success");
          updateAvailability(productId, data.available_quantity);
        } else if (data.status === 'exists') {
          showToast(data.message, 'error');
        } else {
          showToast(data.message || "Error adding to cart", "error");
        }
      })
      .catch(() => {
        showToast("Something went wrong. Please try again.", "error");
      });
    });
  });
});

// Helper: Get CSRF token from cookies
function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return '';
}

// Show toast messages
function showToast(message, type = 'success') {
  const toastContainer = document.querySelector('.toast-container');
  const toast = document.createElement('div');
  toast.className = `toast animate-fade-in ${type === 'error' ? 'error' : ''}`;
  toast.textContent = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// Update availability badge
function updateAvailability(productId, availableQuantity) {
  const availabilityEl = document.getElementById(`availability-${productId}`);
  const button = document.querySelector(`.add-to-cart[data-product-id="${productId}"]`);

  if (availabilityEl) {
    if (availableQuantity > 0) {
      availabilityEl.textContent = `In Stock (${availableQuantity})`;
      availabilityEl.className = 'inline-block px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 fade-update';
      if (button) button.disabled = false;
    } else {
      availabilityEl.textContent = 'Out of Stock';
      availabilityEl.className = 'inline-block px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700 fade-update';
      if (button) button.disabled = true;
    }

    setTimeout(() => {
      availabilityEl.classList.remove('fade-update');
    }, 800);
  }
}

// Optional: updateCartCounter if not defined globally
function updateCartCounter(count) {
  const counter = document.getElementById('cart-counter');
  if (counter) counter.textContent = count;
}
