document.addEventListener('DOMContentLoaded', () => {
  // ---------- Element References ----------
  const imageInput = document.getElementById('image-upload');
  const previewBox = document.getElementById('image-preview-box');
  const uploadText = document.getElementById('upload-text');
  const startDateInput = document.getElementById('start_date');
  const endDateInput = document.getElementById('end_date');
  const cancelBtn = document.querySelector('.cancel-btn');
  const formElement = document.querySelector('.create-form');

  // ---------- Initialize Date Settings ----------
  function initializeDateInputs() {
    const today = new Date().toISOString().split('T')[0];
    startDateInput.min = today;
    endDateInput.min = today;
    
    // Set default values to today and tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    if (!startDateInput.value) {
      startDateInput.value = today;
    }
    
    if (!endDateInput.value) {
      endDateInput.value = tomorrow.toISOString().split('T')[0];
    }
  }
  
  // ---------- Image Preview Functionality ----------
  function setupImageUpload() {
    // File drop functionality
    const preventDefaults = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      previewBox.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
      previewBox.addEventListener(eventName, () => {
        previewBox.classList.add('highlight');
      }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
      previewBox.addEventListener(eventName, () => {
        previewBox.classList.remove('highlight');
      }, false);
    });
    
    previewBox.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length) {
        imageInput.files = files;
        handleImageChange(files[0]);
      }
    }, false);
    
    // Regular file input change
    imageInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
        handleImageChange(this.files[0]);
      }
    });
  }
  
  function handleImageChange(file) {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = function(e) {
        previewBox.style.backgroundImage = `url('${e.target.result}')`;
        uploadText.style.opacity = '0';
        
        // After transition completes, hide element
        setTimeout(() => {
          uploadText.style.display = 'none';
        }, 300);
      };
      reader.readAsDataURL(file);
    } else {
      resetImageUpload();
      if (file) {
        showToast('Please select a valid image file', 'error');
      }
    }
  }
  
  function resetImageUpload() {
    previewBox.style.backgroundImage = '';
    uploadText.style.display = 'flex';
    uploadText.style.opacity = '1';
    imageInput.value = '';
  }
  
  // ---------- Tag System ----------
  function initializeTagSystem() {
    // Get DOM elements
    const tagSearchInput = document.getElementById('tag-search');
    const addTagBtn = document.getElementById('add-tag-btn');
    const tagsInput = document.getElementById('tags');
    const selectedTagsDisplay = document.getElementById('selected-tags-display');
    const tagSuggestions = document.getElementById('tag-suggestions');
    const quickTagButtons = document.querySelectorAll('.quick-tag-btn');
    
    // Store all available tags
    // In a real application, this data would be populated from Django's template context
    // We'll use a sample array for demonstration
    const allTags = [];
    
    // Get tag data from data attributes on quick tag buttons
    quickTagButtons.forEach(btn => {
      const tagName = btn.dataset.tag;
      if (tagName) {
        allTags.push({
          name: tagName,
          count: parseInt(btn.dataset.count || '0', 10)
        });
      }
    });
    
    // Track selected tags
    let selectedTags = [];
    
    // If there are any initial tags, parse them from the hidden input
    if (tagsInput.value) {
      selectedTags = tagsInput.value
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag !== '');
    }
    
    // Initialize hidden input value
    updateHiddenInput();
    
    // Function to add a tag
    function addTag(tagName) {
      tagName = tagName.trim();
      
      // Validate tag
      if (!tagName || tagName.length < 2) return;
      
      // Check if tag already exists
      if (selectedTags.includes(tagName)) return;
      
      // Add to selected tags
      selectedTags.push(tagName);
      
      // Update UI
      updateSelectedTagsDisplay();
      updateHiddenInput();
      
      // Update quick tag buttons
      updateQuickTagButtons();
      
      // Clear search input
      tagSearchInput.value = '';
      
      // Hide suggestions
      tagSuggestions.classList.remove('active');
    }
    
    // Function to remove a tag
    function removeTag(tagName) {
      const tagIndex = selectedTags.indexOf(tagName);
      if (tagIndex !== -1) {
        selectedTags.splice(tagIndex, 1);
        
        // Update UI
        updateSelectedTagsDisplay();
        updateHiddenInput();
        
        // Update quick tag buttons
        updateQuickTagButtons();
      }
    }
    
    // Update hidden input with selected tags
    function updateHiddenInput() {
      tagsInput.value = selectedTags.join(', ');
    }
    
    // Update the display of selected tags
    function updateSelectedTagsDisplay() {
      selectedTagsDisplay.innerHTML = '';
      
      if (selectedTags.length === 0) {
        const noTagsMsg = document.createElement('div');
        noTagsMsg.className = 'no-tags-message';
        noTagsMsg.textContent = 'No tags selected yet';
        selectedTagsDisplay.appendChild(noTagsMsg);
        return;
      }
      
      selectedTags.forEach(tag => {
        const pill = document.createElement('div');
        pill.className = 'tag-pill';
        
        const tagText = document.createElement('span');
        tagText.textContent = tag;
        
        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '×';
        removeBtn.title = 'Remove tag';
        removeBtn.addEventListener('click', () => removeTag(tag));
        
        pill.appendChild(tagText);
        pill.appendChild(removeBtn);
        selectedTagsDisplay.appendChild(pill);
      });
    }
    
    // Update selected state of quick tag buttons
    function updateQuickTagButtons() {
      quickTagButtons.forEach(btn => {
        const tagName = btn.dataset.tag;
        if (selectedTags.includes(tagName)) {
          btn.classList.add('selected');
        } else {
          btn.classList.remove('selected');
        }
      });
    }
    
    // Function to show tag suggestions based on input
    function showSuggestions(query) {
      // Clear suggestions
      tagSuggestions.innerHTML = '';
      
      if (!query || query.length < 2) {
        tagSuggestions.classList.remove('active');
        return;
      }
      
      // Filter tags that match query
      const matchingTags = allTags.filter(tag => 
        tag.name.toLowerCase().includes(query.toLowerCase()) && 
        !selectedTags.includes(tag.name)
      );
      
      if (matchingTags.length === 0) {
        // Show "Create new tag" option
        const createOption = document.createElement('div');
        createOption.className = 'tag-suggestion-item';
        createOption.innerHTML = `Create new tag: <strong>${query}</strong>`;
        createOption.addEventListener('click', () => {
          addTag(query);
        });
        tagSuggestions.appendChild(createOption);
      } else {
        // Show matching tags
        matchingTags.slice(0, 5).forEach(tag => {
          const item = document.createElement('div');
          item.className = 'tag-suggestion-item';
          
          const tagText = document.createElement('span');
          tagText.textContent = tag.name;
          
          const countBadge = document.createElement('span');
          countBadge.className = 'tag-suggestion-count';
          countBadge.textContent = tag.count || 0;
          
          item.appendChild(tagText);
          item.appendChild(countBadge);
          
          item.addEventListener('click', () => {
            addTag(tag.name);
          });
          
          tagSuggestions.appendChild(item);
        });
      }
      
      // Show suggestions dropdown
      tagSuggestions.classList.add('active');
    }
    
    // Event Listeners
    
    // Tag search input
    tagSearchInput.addEventListener('input', () => {
      showSuggestions(tagSearchInput.value.trim());
    });
    
    tagSearchInput.addEventListener('focus', () => {
      if (tagSearchInput.value.trim().length >= 2) {
        showSuggestions(tagSearchInput.value.trim());
      }
    });
    
    // Handle enter key in search input
    tagSearchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        
        // If suggestion is active and visible, click the first one
        const firstSuggestion = tagSuggestions.querySelector('.tag-suggestion-item');
        if (firstSuggestion && tagSuggestions.classList.contains('active')) {
          firstSuggestion.click();
        } else {
          // Otherwise add the current input value as a tag
          addTag(tagSearchInput.value);
        }
      }
    });
    
    // Add tag button
    addTagBtn.addEventListener('click', () => {
      addTag(tagSearchInput.value);
    });
    
    // Quick tag buttons
    quickTagButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const tagName = btn.dataset.tag;
        if (selectedTags.includes(tagName)) {
          removeTag(tagName);
        } else {
          addTag(tagName);
        }
      });
    });
    
    // Close suggestions when clicking outside
    document.addEventListener('click', (e) => {
      if (!tagSearchInput.contains(e.target) && 
          !tagSuggestions.contains(e.target) && 
          e.target !== addTagBtn) {
        tagSuggestions.classList.remove('active');
      }
    });
    
    // Initialize with empty state
    updateSelectedTagsDisplay();
    updateQuickTagButtons();
  }
  
  // ---------- Enhanced Add Tag Button ----------
  function enhanceAddTagButton() {
    const addTagBtn = document.getElementById('add-tag-btn');
    const tagSearchInput = document.getElementById('tag-search');
    
    if (!addTagBtn || !tagSearchInput) return;
    
    // Add button click effect with ripple
    addTagBtn.addEventListener('click', function(e) {
      // Create ripple effect
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      
      // Position the ripple
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      this.appendChild(ripple);
      
      // Remove ripple after animation completes
      setTimeout(() => {
        ripple.remove();
      }, 600);
      
      // Focus the search input after adding a tag
      setTimeout(() => {
        tagSearchInput.focus();
      }, 100);
    });
    
    // Add keyboard shortcut (Alt+A) to add tag
    document.addEventListener('keydown', function(e) {
      if (e.altKey && e.key === 'a') {
        e.preventDefault();
        
        // Add visual feedback
        addTagBtn.classList.add('keyboard-activated');
        setTimeout(() => {
          addTagBtn.classList.remove('keyboard-activated');
        }, 200);
        
        // Trigger button click
        addTagBtn.click();
      }
    });
    
    // Add visual cue when input has content
    tagSearchInput.addEventListener('input', function() {
      if (this.value.trim().length > 0) {
        addTagBtn.classList.add('has-content');
      } else {
        addTagBtn.classList.remove('has-content');
      }
    });
  }
  
  // ---------- Date Validation ----------
  function setupDateValidation() {
    startDateInput.addEventListener('change', function() {
      if (startDateInput.value > endDateInput.value) {
        endDateInput.value = startDateInput.value;
      }
      endDateInput.min = startDateInput.value;
    });
  }
  
  // ---------- Form Actions ----------
  function setupFormActions() {
    // Cancel button
    cancelBtn.addEventListener('click', function(e) {
      e.preventDefault();
      
      const confirmed = confirm('Are you sure you want to cancel? Any unsaved changes will be lost.');
      if (confirmed) {
        window.location.href = '/'; // Redirect to homepage or listing page
      }
    });
    
    // Form validation
    formElement.addEventListener('submit', function(e) {
      const title = document.getElementById('title').value.trim();
      const description = document.getElementById('description').value.trim();
      const image = imageInput.files[0];
      
      if (!title || !description || !startDateInput.value || !endDateInput.value) {
        e.preventDefault();
        showToast('Please fill in all required fields', 'error');
        return;
      }
      
      if (!image) {
        const confirmed = confirm('You haven\'t uploaded an image. Do you want to continue without an image?');
        if (!confirmed) {
          e.preventDefault();
        }
      }
    });
  }
  
  // ---------- Toast Notification System ----------
  function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'toast-container';
      document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    // Add icon based on type
    let icon;
    switch (type) {
      case 'success':
        icon = 'check-circle';
        break;
      case 'error':
        icon = 'exclamation-circle';
        break;
      case 'warning':
        icon = 'exclamation-triangle';
        break;
      default:
        icon = 'info-circle';
    }
    
    toast.innerHTML = `
      <i class="fas fa-${icon}"></i>
      <span>${message}</span>
      <button class="toast-close"><i class="fas fa-times"></i></button>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Show toast with animation
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);
    
    // Handle close button
    toast.querySelector('.toast-close').addEventListener('click', () => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 300);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
      if (toast.parentNode) {
        toast.classList.remove('show');
        setTimeout(() => {
          if (toast.parentNode) {
            toast.remove();
          }
        }, 300);
      }
    }, 5000);
  }
  
  // ---------- Initialize Everything ----------
  function init() {
    initializeDateInputs();
    setupImageUpload();
    initializeTagSystem();
    enhanceAddTagButton();
    setupDateValidation();
    setupFormActions();
  }
  
  // Launch initialization
  init();
});