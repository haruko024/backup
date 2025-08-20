const toggleThemeBtn = document.getElementById("toggleTheme");
toggleThemeBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  toggleThemeBtn.classList.toggle("bx-sun");
  toggleThemeBtn.classList.toggle("bx-moon");
});

// Image Modal Logic
const modal = document.getElementById("imageModal");
const modalImg = document.getElementById("modalImage");
const modalCaption = document.getElementById("modalCaption");
const galleryImages = document.querySelectorAll(".gallery-grid img");
const closeModal = document.querySelector(".modal .close");

let currentIndex = 0;

function openModal(index) {
  currentIndex = index;
  const img = galleryImages[currentIndex];
  modal.style.display = "block";
  modalImg.src = img.src;
  modalCaption.innerHTML = `
    <strong>${img.dataset.country || "Unknown Country"}</strong>
    <p>${img.dataset.description || "No description available."}</p>
  `;
  updateThumbnails();
}

function nextImage() {
  currentIndex = (currentIndex + 1) % galleryImages.length;
  openModal(currentIndex);
}

function selectImage(index) {
  openModal(index);
}

galleryImages.forEach((img, index) => {
  img.addEventListener("click", () => {
    openModal(index);
  });
});

closeModal.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});

// Add Next Button
const nextBtn = document.createElement("i");
nextBtn.className = "bx bx-chevron-right next";
nextBtn.addEventListener("click", nextImage);
document.querySelector(".modal-box").appendChild(nextBtn);

// Add Thumbnail Preview Below Modal
const thumbnailsContainer = document.createElement("div");
thumbnailsContainer.className = "preview-thumbnails";
document.querySelector(".modal-box").appendChild(thumbnailsContainer);

function updateThumbnails() {
  thumbnailsContainer.innerHTML = "";
  galleryImages.forEach((img, idx) => {
    const thumb = document.createElement("img");
    thumb.src = img.src;
    thumb.alt = img.alt;
    thumb.addEventListener("click", () => selectImage(idx));
    thumbnailsContainer.appendChild(thumb);
  });
}
