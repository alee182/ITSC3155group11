  // Mobile sidebar toggle
  const sidebarToggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  
  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener('click', function() {
      sidebar.classList.toggle('active');
    });
  }
  
  // View toggle functionality
  const listViewBtn = document.getElementById('listViewBtn');
  const gridViewBtn = document.getElementById('gridViewBtn');
  const postsContainer = document.getElementById('postsContainer');
  
  listViewBtn.addEventListener('click', function() {
    postsContainer.classList.remove('posts-grid');
    listViewBtn.classList.add('active');
    gridViewBtn.classList.remove('active');
    localStorage.setItem('communityViewMode', 'list');
  });
  
  gridViewBtn.addEventListener('click', function() {
    postsContainer.classList.add('posts-grid');
    gridViewBtn.classList.add('active');
    listViewBtn.classList.remove('active');
    localStorage.setItem('communityViewMode', 'grid');
  });
  
  // Load saved view preference
  document.addEventListener('DOMContentLoaded', function() {
    const savedViewMode = localStorage.getItem('communityViewMode');
    if (savedViewMode === 'grid') {
      postsContainer.classList.add('posts-grid');
      gridViewBtn.classList.add('active');
      listViewBtn.classList.remove('active');
    }
  });
  
  // Hide the debug line that appears at the bottom
  document.addEventListener('DOMContentLoaded', function() {
    const debugEls = document.querySelectorAll('body > div[style*="position: fixed; bottom: 0"]');
    debugEls.forEach(el => el.style.display = 'none');
  });