/**
 * Product Detail Page JavaScript
 * Handles image gallery and wishlist functionality
 */

// Change the main product image when a thumbnail is clicked
function changeImage(imageUrl, thumbnail) {
    // Update main image
    document.getElementById('main-image').src = imageUrl;
    
    // Update active thumbnail
    document.querySelectorAll('.thumbnail').forEach(thumb => {
      thumb.classList.remove('active');
    });
    
    thumbnail.classList.add('active');
  }
  
  // Initialize page elements when DOM is loaded
  document.addEventListener('DOMContentLoaded', function() {
    // Set up wishlist toggle functionality
    const wishlistButton = document.getElementById('wishlistButton');
    
    if (wishlistButton) {
      wishlistButton.addEventListener('click', function() {
        const icon = this.querySelector('i');
        
        if (icon.classList.contains('far')) {
          // Add to wishlist
          icon.classList.remove('far');
          icon.classList.add('fas');
          this.innerHTML = '<i class="fas fa-heart"></i> Added to wishlist';
          
          // Optional: Call API or save to localStorage
          // saveToWishlist(productId);
          
          // Show feedback (optional)
          showNotification('Added to wishlist!');
        } else {
          // Remove from wishlist
          icon.classList.remove('fas');
          icon.classList.add('far');
          this.innerHTML = '<i class="far fa-heart"></i> Add to wishlist';
          
          // Optional: Call API or remove from localStorage
          // removeFromWishlist(productId);
          
          // Show feedback (optional)
          showNotification('Removed from wishlist');
        }
      });
    }
    
    // Check if item is already in wishlist (placeholder function)
    function checkWishlistStatus() {
      // This would typically check localStorage or make an API call
      // For now, we'll just default to "not in wishlist"
      return false;
    }
    
    // Show notification message (optional enhancement)
    function showNotification(message) {
      // Create notification element if it doesn't exist
      let notification = document.querySelector('.notification');
      
      if (!notification) {
        notification = document.createElement('div');
        notification.className = 'notification';
        document.body.appendChild(notification);
        
        // Add styles for notification
        notification.style.position = 'fixed';
        notification.style.bottom = '20px';
        notification.style.right = '20px';
        notification.style.backgroundColor = 'var(--color-main)';
        notification.style.color = 'white';
        notification.style.padding = '10px 20px';
        notification.style.borderRadius = '4px';
        notification.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        notification.style.transform = 'translateY(100px)';
        notification.style.opacity = '0';
        notification.style.transition = 'all 0.3s ease';
      }
      
      // Set message and show notification
      notification.textContent = message;
      
      // Show with animation
      setTimeout(() => {
        notification.style.transform = 'translateY(0)';
        notification.style.opacity = '1';
      }, 10);
      
      // Hide after delay
      setTimeout(() => {
        notification.style.transform = 'translateY(100px)';
        notification.style.opacity = '0';
      }, 3000);
    }
    
    // Initialize the page based on current wishlist status
    if (checkWishlistStatus()) {
      const icon = wishlistButton.querySelector('i');
      icon.classList.remove('far');
      icon.classList.add('fas');
      wishlistButton.innerHTML = '<i class="fas fa-heart"></i> Added to wishlist';
    }
  });