// Edit Sale JavaScript

document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('images');
    const imageCount = document.getElementById('imageCount');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const uploadArea = document.querySelector('.upload-area');
    const form = document.getElementById('saleForm');
    const removedImagesInput = document.getElementById('removedImages');
  
    const removedImages = [];
    let newImages = [];
  
    function updateImageCount() {
      const existingImagesCount = imagePreviewContainer.querySelectorAll('.existing-image').length;
      const newImagesCount = imagePreviewContainer.querySelectorAll('.new-image').length;
      const totalCount = existingImagesCount + newImagesCount;
      imageCount.textContent = totalCount;
  
      if (totalCount >= 5) {
        imageInput.disabled = true;
        uploadArea.classList.add('disabled');
        uploadArea.title = 'Maximum 5 images allowed';
      } else {
        imageInput.disabled = false;
        uploadArea.classList.remove('disabled');
        uploadArea.title = '';
      }
    }
  
    function setupRemoveButtons() {
        const removeButtons = imagePreviewContainer.querySelectorAll('.remove-image[data-id]');
        removeButtons.forEach(button => {
          button.addEventListener('click', function (e) {
            e.preventDefault();
            const imageId = this.getAttribute('data-id');
      
            if (imageId) {
              removedImages.push(imageId);
              removedImagesInput.value = removedImages.join(',');
      
              const preview = this.closest('.image-preview');
              if (preview) {
                preview.remove();
              }
      
              updateImageCount();
            }
          });
        });
      }

  
    imageInput.addEventListener('change', function () {
      handleFiles(this.files);
    });
  
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      uploadArea.addEventListener(eventName, preventDefaults, false);
    });
  
    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }
  
    ['dragenter', 'dragover'].forEach(eventName => {
      uploadArea.addEventListener(eventName, () => uploadArea.classList.add('highlight'), false);
    });
  
    ['dragleave', 'drop'].forEach(eventName => {
      uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('highlight'), false);
    });
  
    uploadArea.addEventListener('drop', function (e) {
      handleFiles(e.dataTransfer.files);
    });
  
    function handleFiles(files) {
      const currentCount = parseInt(imageCount.textContent);
  
      if (currentCount >= 5) {
        showMessage('Maximum 5 images allowed', 'error');
        return;
      }
  
      const remainingSlots = 5 - currentCount;
      const filesToProcess = Math.min(remainingSlots, files.length);
  
      if (files.length > remainingSlots) {
        showMessage(`Only ${remainingSlots} more image(s) can be added`, 'error');
      }
  
      for (let i = 0; i < filesToProcess; i++) {
        const file = files[i];
        if (!file.type.match('image.*')) {
          showMessage('Please select only image files', 'error');
          continue;
        }
        if (file.size > 5 * 1024 * 1024) {
          showMessage('Image files must be less than 5MB', 'error');
          continue;
        }
  
        newImages.push(file);
  
        const reader = new FileReader();
        reader.onload = function (e) {
          const preview = document.createElement('div');
          preview.className = 'image-preview new-image';
  
          const img = document.createElement('img');
          img.src = e.target.result;
          img.alt = 'Preview';
  
          const removeBtn = document.createElement('button');
          removeBtn.className = 'remove-image';
          removeBtn.type = 'button';
          removeBtn.innerHTML = '<i class="fas fa-times"></i>';
  
          removeBtn.addEventListener('click', function () {
            const index = newImages.indexOf(file);
            if (index !== -1) newImages.splice(index, 1);
            preview.remove();
            updateImageCount();
          });
  
          preview.appendChild(img);
          preview.appendChild(removeBtn);
          imagePreviewContainer.appendChild(preview);
  
          updateImageCount();
        };
        reader.readAsDataURL(file);
      }
    }
  
    form.addEventListener('submit', function () {
      removedImagesInput.value = removedImages.join(',');
      updateImageCount();
    });
  
    function showMessage(text, type) {
      let messageContainer = document.querySelector('.message-container');
      if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.className = 'message-container';
        form.prepend(messageContainer);
      }
  
      const message = document.createElement('div');
      message.className = `message ${type}`;
      message.textContent = text;
      message.style.display = 'block';
      messageContainer.appendChild(message);
  
      setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => {
          message.remove();
          if (messageContainer.children.length === 0) {
            messageContainer.remove();
          }
        }, 300);
      }, 3000);
    }
  
    // Initialize
    updateImageCount();
    setupRemoveButtons();
  });