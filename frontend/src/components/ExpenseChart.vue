<template>
  <div class="chart-wrapper">
    <h3>Despesas por Categoria</h3>
    <div class="canvas-container">
      <Pie
        :data="store.expenseChartData"
        :options="chartOptions"
        v-if="store.expenseChartData.datasets[0].data.length > 0"
      />
      <p v-else class="empty-msg">Nenhum gasto para exibir.</p>
    </div>
  </div>
</template>

<script setup>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from "chart.js";
import { useFinanceStore } from "../stores/finance";

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

const store = useFinanceStore();

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // Permite que a gente controle a altura via CSS
  plugins: {
    legend: {
      position: "bottom", // Coloca a legenda embaixo para economizar espaço lateral
    },
  },
};
</script>

<style scoped>
.chart-wrapper {
  background: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  text-align: center;
}

.canvas-container {
  height: 300px; /* IMPORTANTE: Define uma altura fixa para o gráfico */
  position: relative;
}

h3 {
  margin-bottom: 15px;
  font-size: 1.1em;
  color: #2c3e50;
}

.empty-msg {
  padding-top: 50px;
  color: #999;
}
</style>
