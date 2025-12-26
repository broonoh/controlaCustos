<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["income", "expense"]);
const chartCanvas = ref(null);
let chartInstance = null;

const renderChart = () => {
  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(chartCanvas.value, {
    type: "bar",
    data: {
      labels: ["Financeiro"],
      datasets: [
        {
          label: "Receitas",
          data: [props.income],
          backgroundColor: "#10b981",
          borderRadius: 8,
        },
        {
          label: "Despesas",
          data: [props.expense],
          backgroundColor: "#ef4444",
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true, position: "bottom" },
      },
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
};

onMounted(renderChart);
watch(() => [props.income, props.expense], renderChart);
</script>

<style scoped>
.chart-container {
  height: 250px;
  width: 100%;
}
</style>
