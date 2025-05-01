/**
 * Community Page JavaScript
 * This file handles all interactive functionality for the community page
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile sidebar
    initSidebar();
    
    // Initialize view toggle
    initViewToggle();
    
    // Hide debug bar
    hideDebugBar();
    
    // Check for sample tag data if no Django data available
    if (typeof allTags === 'undefined' || allTags.length === 0) {
      console.warn('No tag data found from Django. Using sample data.');
      initTagSearch(getSampleTagData());
    }
  });
  
  /**
   * Initialize sidebar toggle functionality for mobile
   */
  function initSidebar() {
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggleBtn && sidebar) {
      sidebarToggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('active');
      });
    }
  }
  
  /**
   * Initialize view toggle (list/grid) functionality
   */
  function initViewToggle() {
    const listViewBtn = document.getElementById('listViewBtn');
    const gridViewBtn = document.getElementById('gridViewBtn');
    const postsContainer = document.getElementById('postsContainer');
    
    if (listViewBtn && gridViewBtn && postsContainer) {
      // List view button click
      listViewBtn.addEventListener('click', function() {
        postsContainer.classList.remove('posts-grid');
        listViewBtn.classList.add('active');
        gridViewBtn.classList.remove('active');
        localStorage.setItem('communityViewMode', 'list');
      });
      
      // Grid view button click
      gridViewBtn.addEventListener('click', function() {
        postsContainer.classList.add('posts-grid');
        gridViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
        localStorage.setItem('communityViewMode', 'grid');
      });
      
      // Load saved view preference
      const savedViewMode = localStorage.getItem('communityViewMode');
      if (savedViewMode === 'grid') {
        postsContainer.classList.add('posts-grid');
        gridViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
      }
    }
  }
  
  /**
   * Initialize tag search functionality
   * @param {Array} tagData - Array of tag objects with name, count, and icon
   */
  function initTagSearch(tagData) {
    const tagSearchInput = document.getElementById('tagSearchInput');
    const tagSearchResults = document.getElementById('tagSearchResults');
    
    if (!tagSearchInput || !tagSearchResults) {
      console.warn('Tag search elements not found in the DOM');
      return;
    }
    
    // Function to filter tags
    function filterTags(query) {
      if (!query) {
        tagSearchResults.classList.remove('show');
        return;
      }
      
      query = query.toLowerCase();
      const filteredTags = tagData.filter(tag => 
        tag.name.toLowerCase().includes(query)
      );
      
      renderResults(filteredTags);
    }
    
    // Function to render results
    function renderResults(tags) {
      if (tags.length === 0) {
        tagSearchResults.innerHTML = '<div class="no-results">No tags found</div>';
      } else {
        tagSearchResults.innerHTML = '';
        tags.forEach(tag => {
          const tagElement = document.createElement('div');
          tagElement.className = 'tag-result';
          tagElement.innerHTML = `
            <i class="fas ${tag.icon}"></i>
            <span>${tag.name}</span>
            <span class="tag-count">${tag.count}</span>
          `;
          tagElement.addEventListener('click', () => {
            // Navigate to the tag's URL
            window.location.href = `?tag=${tag.name.toLowerCase()}`;
          });
          tagSearchResults.appendChild(tagElement);
        });
      }
      
      tagSearchResults.classList.add('show');
    }
    
    // Event listeners for tag search
    tagSearchInput.addEventListener('input', () => {
      filterTags(tagSearchInput.value);
    });
    
    tagSearchInput.addEventListener('focus', () => {
      if (tagSearchInput.value) {
        filterTags(tagSearchInput.value);
      }
    });
    
    // Close results when clicking outside
    document.addEventListener('click', (e) => {
      if (!tagSearchInput.contains(e.target) && !tagSearchResults.contains(e.target)) {
        tagSearchResults.classList.remove('show');
      }
    });
  }
  
  /**
   * Hide the debug bar at the bottom of the page
   */
  function hideDebugBar() {
    const debugEls = document.querySelectorAll('body > div[style*="position: fixed; bottom: 0"]');
    debugEls.forEach(el => el.style.display = 'none');
  }
  
  /**
   * Get sample tag data if no Django data is available
   * @returns {Array} Sample tag data
   */
  function getSampleTagData() {
    return [
      { name: 'Haircut', count: 5, icon: 'fa-cut' },
      { name: 'Food', count: 8, icon: 'fa-utensils' },
      { name: 'Nails', count: 3, icon: 'fa-hand-sparkles' },
      { name: 'Photography', count: 12, icon: 'fa-camera' },
      { name: 'Events', count: 7, icon: 'fa-calendar-day' },
      { name: 'Tutoring', count: 4, icon: 'fa-book' },
      { name: 'Fitness', count: 6, icon: 'fa-dumbbell' },
      { name: 'Art', count: 9, icon: 'fa-palette' },
      { name: 'Plants', count: 2, icon: 'fa-leaf' }
    ];
  }