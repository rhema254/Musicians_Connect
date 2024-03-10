//----!-Function to change page to Login page from the LandingPage-!!---
document.addEventListener("DOMContentLoaded", function(){

    var openLoginPage = document.getElementById("Login");

    openLoginPage.addEventListener("click", function(){

        var targetURL="Login.html";
        window.open(targetURL, "_self");
    });

});



//----!-function to show/hide password on LoginPAge and NOT YET ADDED!!!------
function myFunction() {
    var x = document.getElementById("myInput");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }


  //----!!-footer function to show only when page is scrolled to the end-!!----
  document.addEventListener('DOMContentLoaded', function () {
  var container = document.querySelector('.container');
  var footer = document.querySelector('.footer');

  function toggleFooter() {
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

    if (scrollTop + clientHeight >= scrollHeight) {
      footer.style.display = 'block';
    } else {
      footer.style.display = 'none';
    }
  }

  window.addEventListener('scroll', toggleFooter);
  window.addEventListener('resize', toggleFooter);
});


// ---!!-Add professions Functionality-!!---

document.addEventListener("DOMContentLoaded", function () {
  // Get elements
  const addProfessionBtn = document.getElementById("add-profession-btn");
  const professionsSelect = document.getElementById("professions");
  const selectedProfessionsContainer = document.getElementById("selected-professions-container");

   // Hide the dropdown initially
  professionsSelect.style.display = "none";

   // Event listener for the "Add" button
  addProfessionBtn.addEventListener("onclick", function () {
    // Toggle the display of the professions dropdown
    professionsSelect.style.display = professionsSelect.style.display === "none" ? "block" : "none";
  });

  // Event listener for profession selection
  professionsSelect.addEventListener("change", function () {
    // Clear existing selected professions
    selectedProfessionsContainer.innerHTML = "";

    // Iterate through selected options and display them
    professionsSelect.selectedOptions.forEach(function (option) {
      const span = document.createElement("span");
      span.textContent = option.value;
      selectedProfessionsContainer.appendChild(span);
    });
  });
});


//------Js code to handle the profile-picture part------
function handleImageUpload(event) {
  const placeholderImage = document.querySelector('#cert-add-btn');
  const uploadedImage = document.querySelector('.uploaded-image');
  const uploadInput = event.target;

  // Check if a file is selected
  if (uploadInput.files && uploadInput.files[0]) {
    const reader = new FileReader();

    // Display the selected image as the uploaded image
    reader.onload = function (e) {
      uploadedImage.src = e.target.result;
      uploadedImage.style.display = 'block';
      placeholderImage.style.display = 'none';
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(uploadInput.files[0]);
  }
}





//------Js code to handle the Video Adding part------
function handleVideoUpload(event) {
  const placeholderIcon = document.querySelector('.placeholder-icon');
  const uploadedVideo = document.querySelector('.uploaded-video');
  const uploadInput = event.target;

  // Check if a file is selected
  if (uploadInput.files && uploadInput.files[0]) {
    const reader = new FileReader();

    // Display the selected video as the uploaded video
    reader.onload = function (e) {
      uploadedVideo.src = e.target.result;
      uploadedVideo.style.display = 'block';
      placeholderIcon.style.display = 'none';
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(uploadInput.files[0]);
  }
}

function showPopup() {
  document.getElementById("popup").style.display = "block";
  }

  function hidePopup() {
      document.getElementById("popup").style.display = "none";
  }
