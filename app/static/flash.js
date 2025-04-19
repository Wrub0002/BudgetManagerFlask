// flash.js
// This script automatically removes flash messages after a certain timeout
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");

  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach((alert) => {
        alert.classList.remove("show");
        alert.classList.add("fade");
        setTimeout(() => alert.remove(), 500);
      });
    }, 3000); // 3 seconds
  }
});

// This script toggles the visibility of the password input field
document.addEventListener("DOMContentLoaded", () => {
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");
  const toggleIcon = document.getElementById("togglePasswordIcon");

  if (togglePassword && passwordInput && toggleIcon) {
    togglePassword.addEventListener("click", () => {
      const isHidden = passwordInput.type === "password";
      passwordInput.type = isHidden ? "text" : "password";
      toggleIcon.classList.toggle("fa-eye");
      toggleIcon.classList.toggle("fa-eye-slash");
    });
  }
});

