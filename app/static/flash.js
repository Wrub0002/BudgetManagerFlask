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

  // === Main Chart Logic with Category Colors ===
 // === Render the main chart using Chart.js ===
const ctx = document.getElementById("mainChart");
if (ctx) {
  const chartSelector = document.getElementById("chartSelector");

  const categoryColorMap = {
    Food: "#FF6B6B",
    Transport: "#4D96FF",
    Housing: "#6C5CE7",
    Entertainment: "#FFA630",
    Healthcare: "#2ED573",
    Clothing: "#5F27CD",
    Education: "#1E90FF",
    Subscriptions: "#636E72",
    Other: "#FDCB6E",
    Salary: "#A29BFE",
    Investment: "#74B9FF",
    Gift: "#FF7675",
    "Side Job": "#55EFC4",
    Rental: "#81ECEC",
    Interest: "#FAB1A0",
    Dividends: "#E17055",
    Bonus: "#FD79A8",
    Freelance: "#00CEC9"
  };

  const generateColors = (labels) => {
    return labels.map(label => categoryColorMap[label] || "#CCCCCC");
  };

  const dataSets = {
    expenses: {
      labels: chartData.expenses.labels,
      data: chartData.expenses.values,
      label: "Expenses",
      get bgColor() {
        return generateColors(this.labels);
      }
    },
    income: {
      labels: chartData.income.labels,
      data: chartData.income.values,
      label: "Income",
      get bgColor() {
        return generateColors(this.labels);
      }
    },
    totals: {
      labels: ["Income", "Expenses"],
      datasets: [
        {
          label: "Income",
          data: [chartData.totals.values[0], 0],
          backgroundColor: "rgba(75, 192, 192, 0.5)"
        },
        {
          label: "Expenses",
          data: [0, chartData.totals.values[1]],
          backgroundColor: "rgba(255, 99, 132, 0.5)"
        }
      ]
    }
  };

  let chart = new Chart(ctx.getContext("2d"), {
    type: "bar",
    data: {
      labels: dataSets.expenses.labels,
      datasets: [
        {
          label: dataSets.expenses.label,
          data: dataSets.expenses.data,
          backgroundColor: dataSets.expenses.bgColor,
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total Income vs Expenses"
        },
        legend: {
          labels: {
            usePointStyle: true
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          ticks: {
            align: "center"
          }
        },
        y: {
          stacked: true,
          beginAtZero: true
        }
      }
    }
  });

  function updateChart(type) {
  const selectedData = dataSets[type];
  chart.data.labels = selectedData.labels;
    chart.data.labels = selectedData.labels;

    if (type === "totals") {
      chart.data.datasets = selectedData.datasets;
    } else {
      chart.data.datasets = [{
        label: selectedData.label,
        data: selectedData.data,
        backgroundColor: typeof selectedData.bgColor === "function"
          ? selectedData.bgColor()
          : selectedData.bgColor
      }];
    }


  chart.options.plugins.title.text =
    chartSelector.options[chartSelector.selectedIndex].text;

  // 👇 Mostrar legenda só para o gráfico de comparação total
  chart.options.plugins.legend.display = type === "totals";

  chart.update();
}


  chartSelector.addEventListener("change", function () {
    updateChart(this.value);
  });
}
});