document.addEventListener("DOMContentLoaded", function () {
  // Automatically removes flash messages after a certain timeout
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

  // Toggles the visibility of the password input field
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

  // Trims whitespace from the username input on form submission
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function () {
      const usernameInput = document.querySelector("#username");
      if (usernameInput) {
        usernameInput.value = usernameInput.value.trim();
      }
    });
  }

  // Initializes the income/expense chart
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