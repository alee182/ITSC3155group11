 // Image preview functionality with 5 image limit
 const imageInput = document.getElementById('images');
 const previewContainer = document.getElementById('imagePreviewContainer');
 const imageCountDisplay = document.getElementById('imageCount');
 const MAX_IMAGES = 5;
 let selectedFiles = [];
 
 imageInput.addEventListener('change', function() {
   // Get currently selected files
   const newFiles = Array.from(this.files);
   
   // Check if adding new files would exceed the limit
   if (selectedFiles.length + newFiles.length > MAX_IMAGES) {
     alert(`You can only upload a maximum of ${MAX_IMAGES} images. Please select fewer images.`);
     return;
   }
   
   // Add new files to our selected files array
   selectedFiles = [...selectedFiles, ...newFiles];
   
   // If somehow we still have too many, trim the array
   if (selectedFiles.length > MAX_IMAGES) {
     selectedFiles = selectedFiles.slice(0, MAX_IMAGES);
   }
   
   // Update the count display
   imageCountDisplay.textContent = selectedFiles.length;
   
   // Clear and rebuild the preview container
   updateImagePreviews();
 });
 
 function updateImagePreviews() {
   previewContainer.innerHTML = '';
   
   selectedFiles.forEach((file, index) => {
     const reader = new FileReader();
     
     reader.onload = function(event) {
       const previewDiv = document.createElement('div');
       previewDiv.className = 'image-preview';
       
       const img = document.createElement('img');
       img.src = event.target.result;
       
       const removeBtn = document.createElement('button');
       removeBtn.className = 'remove-image';
       removeBtn.innerHTML = '<i class="fas fa-times"></i>';
       
       removeBtn.addEventListener('click', function(e) {
         e.preventDefault();
         // Remove this file from our selectedFiles array
         selectedFiles.splice(index, 1);
         // Update image count
         imageCountDisplay.textContent = selectedFiles.length;
         // Rebuild the previews
         updateImagePreviews();
       });
       
       previewDiv.appendChild(img);
       previewDiv.appendChild(removeBtn);
       previewContainer.appendChild(previewDiv);
     }
     
     reader.readAsDataURL(file);
   });
   
   // Create a DataTransfer object and add our files to it
   // This allows us to update the actual input's files
   const dataTransfer = new DataTransfer();
   selectedFiles.forEach(file => {
     dataTransfer.items.add(file);
   });
   
   // Set the input's files to our curated list
   imageInput.files = dataTransfer.files;
 }
 
 // Category icon display
 const categorySelect = document.getElementById('id_category');
 
 categorySelect.addEventListener('change', function() {
   const iconClass = getCategoryIconClass(this.value);
   this.className = 'with-icon';
   
   // Remove previous icon if exists
   const previousIcon = this.parentElement.querySelector('.category-icon');
   if (previousIcon) {
     previousIcon.remove();
   }
   
   // Add new icon
   const iconSpan = document.createElement('span');
   iconSpan.className = 'category-icon';
   iconSpan.innerHTML = `<i class="${iconClass}"></i>`;
   
   this.parentElement.appendChild(iconSpan);
 });
 
 function getCategoryIconClass(category) {
   switch(category) {
     case 'electronics': return 'fas fa-laptop';
     case 'books': return 'fas fa-book';
     case 'furniture': return 'fas fa-couch';
     case 'clothing': return 'fas fa-tshirt';
     case 'sports': return 'fas fa-basketball-ball';
     case 'other': 
     default: return 'fas fa-ellipsis-h';
   }
 }