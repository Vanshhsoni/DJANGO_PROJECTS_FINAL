document.addEventListener('DOMContentLoaded', function() {
  'use strict';

  window.openModal = function(weaponName, weaponDetails, imageUrl) {
      const modal = document.getElementById("myModal");

      // Set the weapon name
      const modalTitle = document.getElementById("modalTitle");
      if (modalTitle) {
          modalTitle.textContent = weaponName;
      } else {
          console.error("Element with ID 'modalTitle' not found.");
      }

      // Set the weapon details
      const modalDetails = document.getElementById("modalDetails");
      if (modalDetails) {
          modalDetails.textContent = weaponDetails;
      } else {
          console.error("Element with ID 'modalDetails' not found.");
      }

      // Set the weapon image
      const modalImage = document.getElementById("modalImage");
      if (modalImage) {
          modalImage.src = imageUrl;
      } else {
          console.error("Element with ID 'modalImage' not found.");
      }

      // Set the weapon name to the input field
      const modalTitleInput = document.getElementById('modalTitleInput');
      if (modalTitleInput) {
          modalTitleInput.value = weaponName;
      } else {
          console.error("Element with ID 'modalTitleInput' not found.");
      }

      // Update the form action
      const form = document.getElementById('modalForm');
      form.action = `/buy/${weaponName}/`;

      // Show the modal
      modal.style.display = "block";
  };

  window.submitModalForm = function(button) {
      const modalTitleText = document.getElementById('modalTitle').textContent;
      const modalTitleInput = document.getElementById('modalTitleInput');
      if (modalTitleInput) {
          modalTitleInput.value = modalTitleText;
      } else {
          console.error("Element with ID 'modalTitleInput' not found.");
      }
      console.log("Sending Modal Title:", modalTitleText);

      // Submit the form to the server
      const form = document.getElementById('modalForm');
      if (form) {
          form.submit();
      } else {
          console.error("Form with ID 'modalForm' not found.");
      }

      // Optionally navigate to the buy URL after form submission
      const buyUrl = button.getAttribute('data-buy-url');
      if (buyUrl) {
          setTimeout(() => {
              console.log("Redirecting to:", buyUrl);
              window.location.href = buyUrl;
          }, 100); // Delay for 100 ms (adjust as needed)
      }
  };
});
