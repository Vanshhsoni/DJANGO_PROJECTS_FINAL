function previewImage(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const profilePic = document.querySelector('.profile-pic img');
        if (profilePic) {
            profilePic.src = e.target.result;
            profilePic.style.display = 'block'; // Show the selected image
        }
        const span = document.querySelector('.profile-pic span');
        if (span) {
            span.style.display = 'none'; // Hide the '+' when an image is selected
        }
    };
    reader.readAsDataURL(file);
}
