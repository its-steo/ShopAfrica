document.addEventListener('DOMContentLoaded', () => {
    // Initialize favorites from localStorage or empty array
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    updateFavoritesCounter();

    // Favorite button listeners
    document.querySelectorAll('.favourite').forEach(button => {
        const productId = button.getAttribute('data-product-id');
        // Set initial icon state
        if (favorites.includes(productId)) {
            button.querySelector('i').classList.replace('fas', 'far');
        }

        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product-id');
            const icon = button.querySelector('i');
            if (favorites.includes(productId)) {
                // Remove from favorites
                favorites = favorites.filter(id => id !== productId);
                icon.classList.replace('far', 'fas');
                localStorage.setItem('favorites', JSON.stringify(favorites));
                updateFavoritesCounter();
                showToast(`Product ${productId} removed from favorites!`, 'favourite');
            } else {
                // Add to favorites
                favorites.push(productId);
                icon.classList.replace('fas', 'far');
                localStorage.setItem('favorites', JSON.stringify(favorites));
                updateFavoritesCounter();
                showToast(`Product ${productId} added to favorites!`, 'favourite');
            }
        });
    });

    // Update favorites counter in navbar
    function updateFavoritesCounter() {
        const favCounter = document.querySelector('.fav-counter');
        favCounter.textContent = favorites.length;
    }

    // Show toast notification
    function showToast(message, type, isError = false) {
        const toastContainer = document.querySelector('.toast-container');
        const toast = document.createElement('div');
                toast.className = `toast toast-${type} ${isError ? 'toast-error' : ''}`;
                toast.textContent = message;
                toastContainer.appendChild(toast);
        
                setTimeout(() => {
                    toast.remove();
                }, 3000);
            }
        });