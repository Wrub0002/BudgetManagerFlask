// flash.js
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
