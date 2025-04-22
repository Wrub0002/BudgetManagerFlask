document.addEventListener("DOMContentLoaded", function () {
  // === Auto-hide flash messages after a delay ===
  const alerts = document.querySelectorAll(".alert");
  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach((alert) => {
        alert.classList.remove("show");
        alert.classList.add("fade");
        setTimeout(() => alert.remove(), 500);
      });
    }, 3000);
  }

  // === Toggle visibility of password field ===
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

  // === Trim whitespace from username input before form submission ===
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function () {
      const usernameInput = document.querySelector("#username");
      if (usernameInput) {
        usernameInput.value = usernameInput.value.trim();
      }
    });
  }

  // === Render the income/expense chart using Chart.js ===
  const ctx = document.getElementById("incomeExpenseChart");
  if (ctx) {
    const backgroundColors = [
      "#FF6B6B", // Food
      "#4D96FF", // Transport
      "#6C5CE7", // Housing
      "#FFA630", // Entertainment
      "#2ED573", // Healthcare
      "#5F27CD", // Clothing
      "#1E90FF", // Education
      "#636E72", // Subscriptions
      "#FDCB6E", // Other
    ];

    // Labels and values are injected as data-* attributes for flexibility
    const labels = JSON.parse(ctx.dataset.labels);
    const values = JSON.parse(ctx.dataset.values);

    const chart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Expenses",
            backgroundColor: backgroundColors.slice(0, labels.length),
            data: values,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Expenses by Category",
          },
        },
      },
    });
  }
});
