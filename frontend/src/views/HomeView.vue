<template>
  <div class="app-container">
    <header class="main-header">
      <div class="title-group">
        <h1>💰 ProjetoCustos</h1>
      </div>

      <div class="header-actions">
        <div class="filters">
          <select v-model="fMonth" class="mini-select">
            <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
          </select>
          <select v-model="fYear" class="mini-select">
            <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
        <div class="header-actions">
          <button
            @click="exportToPDF"
            class="btn-pdf"
            :disabled="isGenerating"
            :class="{ 'btn-loading': isGenerating }"
          >
            <span v-if="!isGenerating">Exportar PDF 📄</span>
            <span v-else>Gerando Arquivo... ⏳</span>
          </button>
        </div>
        <!-- <button @click="handleLogout" class="btn-logout">Sair 👋</button> -->
      </div>
    </header>

    <section class="summary-grid">
      <div class="s-card b-blue">
        <span class="label">Saldo Atual</span>
        <p :class="(store.summary?.balance || 0) >= 0 ? 'text-pos' : 'text-neg'">
          R$ {{ (store.summary?.balance || 0).toFixed(2) }}
        </p>
      </div>
      <div class="s-card b-green">
        <span class="label">Receitas</span>
        <p class="text-pos">R$ {{ (store.summary?.income || 0).toFixed(2) }}</p>
      </div>
      <div class="s-card b-red">
        <span class="label">Despesas</span>
        <p class="text-neg">R$ {{ (store.summary?.expense || 0).toFixed(2) }}</p>
      </div>
    </section>

    <div class="dashboard-content">
      <section class="card history-card">
        <div class="card-header">
          <h3>Histórico de Lançamentos</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Data</th>
                <th>Descrição</th>
                <th>Valor</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in filtered" :key="t.id">
                <td>{{ new Date(t.date).toLocaleDateString("pt-BR") }}</td>
                <td>
                  <div class="desc-cell">
                    <strong>{{ t.description }}</strong>
                    <span class="cat-tag" :style="{ backgroundColor: getCat(t.category_id).color }">
                      {{ getCat(t.category_id).name }}
                    </span>
                  </div>
                </td>
                <td :class="t.type" class="text-bold">
                  {{ t.type === "expense" ? "-" : "+" }} R$ {{ t.amount.toFixed(2) }}
                </td>
                <td class="actions-cell">
                  <button @click="openEdit(t)" class="btn-icon">✏️</button>
                  <button @click="handleDelete(t.id)" class="btn-icon">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <aside class="sidebar-content">
        <div class="card chart-card">
          <h3>Distribuição</h3>
          <CategoryChart :transactions="filtered" :categories="store.categories" />
        </div>

        <!-- <div class="card categories-nav-card">
          <div class="card-header-flex">
            <h3>Categorias</h3>
            <router-link to="/categories" class="btn-manage">Gerenciar ⚙️</router-link>
          </div>
          <p class="info-text">Configure nomes, cores e remova categorias personalizadas.</p>
        </div> -->

        <div class="card form-card">
          <h3>Novo Registro</h3>
          <form @submit.prevent="handleCreate" class="form-compact">
            <input v-model="form.description" placeholder="Descrição" required />
            <input
              v-model.number="form.amount"
              type="number"
              step="0.01"
              placeholder="Valor R$"
              required
            />
            <div class="form-row">
              <select v-model="form.type">
                <option value="expense">Despesa</option>
                <option value="income">Receita</option>
              </select>
              <select v-model="form.category_id" required>
                <option value="" disabled>Categoria</option>
                <option v-for="c in store.categories" :key="c.id" :value="c.id">
                  {{ c.name }}
                </option>
              </select>
            </div>
            <button type="submit" class="btn-primary" :disabled="loading">Adicionar</button>
          </form>
        </div>
        <div class="card chart-card">
          <h3>Comparativo Mensal</h3>
          <SummaryChart
            :income="store.summary?.income || 0"
            :expense="store.summary?.expense || 0"
          />
        </div>
      </aside>
    </div>

    <EditModal
      v-if="showModal"
      :show="showModal"
      :transaction="toEdit"
      :categories="store.categories"
      @close="showModal = false"
      @save="handleUpdate"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useFinanceStore } from "../stores/finance";
import { useRouter } from "vue-router";
import CategoryChart from "../components/CategoryChart.vue";
import EditModal from "../components/EditModal.vue";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable"; // Importa como uma função separada
// No seu <script setup>
const isGenerating = ref(false);

const exportToPDF = async () => {
  if (isGenerating.value) return;

  isGenerating.value = true;
  try {
    if (!filtered.value || filtered.value.length === 0) {
      alert("Não há transações filtradas para exportar neste período.");
      return;
    }

    const doc = new jsPDF();
    const months = [
      "Janeiro",
      "Fevereiro",
      "Março",
      "Abril",
      "Maio",
      "Junho",
      "Julho",
      "Agosto",
      "Setembro",
      "Outubro",
      "Novembro",
      "Dezembro",
    ];
    const monthName = months[fMonth.value - 1];

    // Cabeçalho do PDF
    doc.setFontSize(18);
    doc.setTextColor(30, 41, 59); // Cor Slate-800
    doc.text(`Relatório Financeiro: ${monthName} / ${fYear.value}`, 14, 20);

    // Linha de Resumo
    doc.setFontSize(11);
    doc.setTextColor(100);
    doc.text(`Gerado em: ${new Date().toLocaleString("pt-BR")}`, 14, 28);
    doc.text(`Saldo do Período: R$ ${store.summary.balance.toFixed(2)}`, 14, 34);

    const tableRows = filtered.value.map((t) => {
      const category = store.categories.find((c) => c.id === t.category_id);
      return [
        new Date(t.date).toLocaleDateString("pt-BR"),
        t.description,
        category ? category.name : "Sem Categoria",
        t.type === "income" ? "Receita" : "Despesa",
        `R$ ${t.amount.toFixed(2)}`,
      ];
    });

    autoTable(doc, {
      startY: 40,
      head: [["Data", "Descrição", "Categoria", "Tipo", "Valor"]],
      body: tableRows,
      headStyles: { fillColor: [30, 41, 59], fontStyle: "bold" },
      alternateRowStyles: { fillColor: [248, 250, 252] },
      margin: { top: 40 },
    });

    doc.save(`Relatorio_${monthName}_${fYear.value}.pdf`);

    // Feedback de sucesso (opcional)
    console.log("PDF gerado com sucesso!");
  } catch (error) {
    console.error("Erro ao gerar PDF:", error);
    alert("Falha ao gerar relatório.");
  } finally {
    isGenerating.value = false;
  }
};
const store = useFinanceStore();
const router = useRouter();

const months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
const currentYear = new Date().getFullYear();
const availableYears = computed(() => [currentYear, currentYear + 1]);

const fMonth = ref(new Date().getMonth() + 1);
const fYear = ref(currentYear);

const showModal = ref(false);
const loading = ref(false);
const toEdit = ref(null);
const form = ref({ description: "", amount: null, type: "expense", category_id: "" });

onMounted(async () => {
  if (store.token) await store.fetchInitialData();
  else router.push("/login");
});

const filtered = computed(() => {
  return store.transactions.filter((t) => {
    const d = new Date(t.date);
    return d.getMonth() + 1 === fMonth.value && d.getFullYear() === fYear.value;
  });
});

const getCat = (id) => {
  return store.categories.find((c) => c.id === id) || { name: "Sem Cat.", color: "#94a3b8" };
};

const handleLogout = () => {
  if (confirm("Deseja sair?")) {
    store.logout();
    router.push("/login");
  }
};

const handleCreate = async () => {
  loading.value = true;
  await store.addTransaction(form.value);
  form.value = { description: "", amount: null, type: "expense", category_id: "" };
  await store.fetchSummary();
  loading.value = false;
};

const openEdit = (t) => {
  toEdit.value = { ...t };
  showModal.value = true;
};
const handleUpdate = async (data) => {
  await store.updateTransaction(data.id, data);
  showModal.value = false;
  await store.fetchSummary();
};
const handleDelete = async (id) => {
  if (confirm("Excluir transação?")) {
    await store.deleteTransaction(id);
    await store.fetchSummary();
  }
};
</script>

<style scoped>
.app-container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8fafc;
  min-height: 100vh;
}
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}
.header-actions {
  padding: 8px 15px;
  background: #97a2adff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.header-actions:hover {
  background: #1a76d1ff;
}
.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.filters select {
  padding: 8px 15px;
  background: #34495e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.filters select:hover {
  background: #2c3e50;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}
.s-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}
.s-card p {
  font-size: 1.8rem;
  font-weight: 800;
  margin-top: 10px;
}
.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 30px;
}
.card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

/* Estilo do Botão de Gerenciar Categorias */
.card-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.btn-manage {
  font-size: 0.85rem;
  padding: 6px 12px;
  background: #f1f5f9;
  color: #475569;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  border: 1px solid #e2e8f0;
}
.btn-manage:hover {
  background: #e2e8f0;
}
.info-text {
  font-size: 0.8rem;
  color: #94a3b8;
  line-height: 1.4;
}

.table-container {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th {
  text-align: left;
  padding: 12px;
  border-bottom: 2px solid #f1f5f9;
  color: #64748b;
  font-size: 0.85rem;
}
td {
  padding: 15px 12px;
  border-bottom: 1px solid #f1f5f9;
}
.cat-tag {
  padding: 4px 10px;
  border-radius: 20px;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  margin-left: 8px;
}

.form-compact input,
.form-compact select {
  width: 100%;
  padding: 12px;
  margin-bottom: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.btn-primary {
  width: 100%;
  padding: 12px;
  background: #1e293b;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}
.btn-logout {
  padding: 8px 16px;
  background: #fee2e2;
  color: #ef4444;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
}
.b-blue {
  border-top: 5px solid #3b82f6;
}
.b-green {
  border-top: 5px solid #10b981;
}
.b-red {
  border-top: 5px solid #ef4444;
}
.text-pos {
  color: #10b981;
}
.text-neg {
  color: #ef4444;
}
.btn-pdf {
  padding: 8px 15px;
  background: #34495e;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s;
}
.btn-pdf:hover {
  background: #2c3e50;
}
.btn-pdf:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  opacity: 0.8;
}

.btn-loading {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.98);
  }
  100% {
    transform: scale(1);
  }
}
</style>
