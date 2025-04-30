   // View toggle functionality
   document.querySelectorAll('.view-btn').forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.remove('active');
      });
      
      // Add active class to clicked button
      this.classList.add('active');
      
      // Change grid view
      const view = this.getAttribute('data-view');
      const productGrid = document.getElementById('productGrid');
      
      if (view === 'list') {
        productGrid.classList.add('list-view');
      } else {
        productGrid.classList.remove('list-view');
      }
    });
  });
  
  // Sort dropdown functionality
  const sortBtn = document.querySelector('.sort-btn');
  const dropdownContent = document.querySelector('.dropdown-content');
  
  if (sortBtn) {
    sortBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      dropdownContent.classList.toggle('show');
    });
  }
  
  // Close dropdown when clicking outside
  window.addEventListener('click', function() {
    if (dropdownContent && dropdownContent.classList.contains('show')) {
      dropdownContent.classList.remove('show');
    }
  });
  
  // Wishlist functionality
  document.querySelectorAll('.wishlist-btn').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const icon = this.querySelector('i');
      if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
      } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
      }
    });
  });