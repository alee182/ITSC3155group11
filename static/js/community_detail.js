/**
 * Community Detail Page JavaScript
 * Enhanced with animations and interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Like button functionality
    const likeButton = document.querySelector('.like-button');
    if (likeButton) {
      likeButton.addEventListener('click', function() {
        const icon = this.querySelector('i');
        
        // Toggle active state
        if (this.classList.contains('active')) {
          this.classList.remove('active');
          icon.classList.remove('fas');
          icon.classList.add('far');
        } else {
          this.classList.add('active');
          icon.classList.remove('far');
          icon.classList.add('fas');
          
          // If dislike is active, remove it
          if (dislikeButton.classList.contains('active')) {
            dislikeButton.classList.remove('active');
            dislikeButton.querySelector('i').classList.remove('fas');
            dislikeButton.querySelector('i').classList.add('far');
          }
        }
        
        // Add micro-animation
        animateButton(this);
        
        // Here you would send an AJAX request to update the server
        // updateReaction('like', getPostId(), this.classList.contains('active'));
      });
    }
    
    // Dislike button functionality
    const dislikeButton = document.querySelector('.dislike-button');
    if (dislikeButton) {
      dislikeButton.addEventListener('click', function() {
        const icon = this.querySelector('i');
        
        // Toggle active state
        if (this.classList.contains('active')) {
          this.classList.remove('active');
          icon.classList.remove('fas');
          icon.classList.add('far');
        } else {
          this.classList.add('active');
          icon.classList.remove('far');
          icon.classList.add('fas');
          
          // If like is active, remove it
          if (likeButton.classList.contains('active')) {
            likeButton.classList.remove('active');
            likeButton.querySelector('i').classList.remove('fas');
            likeButton.querySelector('i').classList.add('far');
          }
        }
        
        // Add micro-animation
        animateButton(this);
        
        // Here you would send an AJAX request to the server
        // updateReaction('dislike', getPostId(), this.classList.contains('active'));
      });
    }
    
    // Share button functionality
    const shareButton = document.querySelector('.share-button');
    if (shareButton) {
      shareButton.addEventListener('click', function() {
        const url = window.location.href;
        
        // Add micro-animation
        animateButton(this);
        
        // Try to use the Web Share API if available
        if (navigator.share) {
          navigator.share({
            title: document.title,
            url: url
          })
          .then(() => console.log('Successful share'))
          .catch(error => console.log('Error sharing:', error));
        } else {
          // Fallback - copy to clipboard
          navigator.clipboard.writeText(url)
            .then(() => {
              // Show a toast notification
              showToast('Link copied to clipboard!');
            })
            .catch(err => {
              console.error('Failed to copy: ', err);
              showToast('Failed to copy link');
            });
        }
      });
    }
    
    // Comment form enhancements
    const commentForm = document.querySelector('.comment-form');
    const commentTextarea = document.querySelector('.comment-form textarea');
    
    if (commentTextarea) {
      // Auto-expand textarea as user types
      commentTextarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
      });
      
      // Focus effects
      commentTextarea.addEventListener('focus', function() {
        commentForm.classList.add('focused');
      });
      
      commentTextarea.addEventListener('blur', function() {
        commentForm.classList.remove('focused');
      });
    }
    
    // Animation for buttons on click
    function animateButton(button) {
      button.classList.add('clicked');
      setTimeout(() => {
        button.classList.remove('clicked');
      }, 300);
    }
    
    // Add button click animation styles
    if (!document.getElementById('animation-styles')) {
      const style = document.createElement('style');
      style.id = 'animation-styles';
      style.textContent = `
        .like-button.clicked,
        .dislike-button.clicked,
        .share-button.clicked {
          transform: scale(0.95);
        }
        .comment-form.focused textarea {
          border-color: var(--color-accent);
          box-shadow: 0 0 0 3px rgba(241, 230, 178, 0.3);
        }
      `;
      document.head.appendChild(style);
    }
    
    // Helper function to get CSRF token for AJAX requests
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    
    // Helper function to get post ID from URL
    function getPostId() {
      const pathParts = window.location.pathname.split('/');
      // Return post ID based on URL structure
      // Adjust this based on your actual URL structure
      for (let i = 0; i < pathParts.length; i++) {
        if (pathParts[i] === 'post' || pathParts[i] === 'community') {
          return pathParts[i + 1];
        }
      }
      return null;
    }
    
    // Helper function to show toast notification
    function showToast(message) {
      // Create toast element if it doesn't exist
      let toast = document.querySelector('.toast');
      
      if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast';
        document.body.appendChild(toast);
      }
      
      // Update message and show
      toast.textContent = message;
      
      // Reset any existing animations
      toast.classList.remove('show');
      
      // Force reflow
      void toast.offsetWidth;
      
      // Show the toast
      setTimeout(() => {
        toast.classList.add('show');
      }, 10);
      
      // Hide the toast after 3 seconds
      setTimeout(() => {
        toast.classList.remove('show');
      }, 3000);
    }
    
    // Add entrance animations for comments
    const comments = document.querySelectorAll('.comment');
    
    if (comments.length > 0) {
      // Add animation styles if not already present
      if (!document.getElementById('comment-animation-styles')) {
        const style = document.createElement('style');
        style.id = 'comment-animation-styles';
        style.textContent = `
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          .comment {
            animation: fadeInUp 0.4s ease forwards;
            opacity: 0;
          }
        `;
        document.head.appendChild(style);
      }
      
      // Set staggered animation delay for each comment
      comments.forEach((comment, index) => {
        comment.style.animationDelay = `${index * 0.1}s`;
      });
    }
  });