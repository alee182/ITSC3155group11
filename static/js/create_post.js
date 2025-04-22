document.addEventListener('DOMContentLoaded', () => {
  // ---------- Image Preview ----------
  const imageInput = document.getElementById('image-upload');
  const previewBox = document.getElementById('image-preview-box');
  const uploadText = document.getElementById('upload-text');

  imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewBox.style.backgroundImage = `url('${e.target.result}')`;
        uploadText.style.display = 'none';
      };
      reader.readAsDataURL(file);
    } else {
      previewBox.style.backgroundImage = '';
      uploadText.style.display = 'block';
    }
  });

  // ---------- Tag Logic ----------
  const tagSelect = document.getElementById('tag-select');
  const tagInput = document.getElementById('tags');

  tagSelect.addEventListener('change', () => {
    const selected = Array.from(tagSelect.selectedOptions).map(opt => opt.value);
    const typedTags = tagInput.value
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag !== '');

    // Combine selected + manual, remove duplicates
    const combined = [...new Set([...typedTags, ...selected])];
    tagInput.value = combined.join(', ');
  });
});
