const toggleBtn = document.getElementById("toggleDark");

function updateButtonLabel() {
  const isDark = document.body.classList.contains("dark");
  toggleBtn.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
}

toggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  updateButtonLabel();
});

updateButtonLabel();
