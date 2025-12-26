<template>
  <div class="chart-container">
    <Doughnut v-if="hasData" :data="chartData" :options="chartOptions" />
    <p v-else class="no-data">Sem despesas neste período</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { Doughnut } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps(["transactions", "categories"]);

const hasData = computed(() => props.transactions.some((t) => t.type === "expense"));

const chartData = computed(() => {
  const expenses = props.transactions.filter((t) => t.type === "expense");

  // Agrupar valores por categoria
  const totals = {};
  expenses.forEach((t) => {
    totals[t.category_id] = (totals[t.category_id] || 0) + t.amount;
  });

  const labels = [];
  const data = [];
  const colors = [];

  Object.keys(totals).forEach((catId) => {
    const category = props.categories.find((c) => c.id == catId);
    labels.push(category ? category.name : "Outros");
    data.push(totals[catId]);
    colors.push(category ? category.color : "#cbd5e0");
  });

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: colors,
        borderWidth: 1,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: "bottom" },
  },
};
</script>

<style scoped>
.chart-container {
  height: 300px;
  position: relative;
  margin-top: 20px;
}
.no-data {
  text-align: center;
  color: #7f8c8d;
  padding-top: 100px;
}
</style>
