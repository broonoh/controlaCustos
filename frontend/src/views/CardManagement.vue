<template>
  <div class="app-container">
    <header class="header-section">
      <div class="title-group">
        <h1>Terceiros</h1>
        <p class="subtitle">Gerencie gastos de outras pessoas no seu cartão</p>
      </div>

      <div class="add-person-box">
        <input v-model="novaPessoa" placeholder="Nome da pessoa..." @keyup.enter="criarAba" />
        <button @click="criarAba" class="btn-add">Adicionar</button>
      </div>
    </header>

    <nav class="tabs-nav">
      <div
        v-for="pessoa in pessoas"
        :key="pessoa.id"
        class="tab-pill"
        :class="{ active: abaAtiva?.id === pessoa.id }"
        @click="selecionarPessoa(pessoa)"
      >
        <input
          v-if="editandoAbaId === pessoa.id"
          v-model="pessoa.name"
          @blur="salvarNomeAba(pessoa)"
          @keyup.enter="salvarNomeAba(pessoa)"
          v-focus
          class="input-tab-edit"
        />
        <span v-else @dblclick="iniciarEdicaoAba(pessoa)">
          {{ pessoa.name }}
        </span>

        <button class="btn-remove-tab" @click.stop="deletarPessoa(pessoa.id)">×</button>
      </div>
    </nav>

    <main v-if="abaAtiva" class="table-card">
      <div class="card-header">
        <div class="info">
          <h3>Lançamentos: {{ abaAtiva.name }}</h3>
          <span class="total-badge">Total: R$ {{ totalGasto.toFixed(2) }}</span>
        </div>
        <button @click="adicionarLinhaGasto" class="btn-new-entry">+ Novo Gasto</button>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Descrição</th>
              <th>Categoria</th>
              <th>Valor</th>
              <th>Data</th>
              <th class="text-center">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="gasto in gastosPessoa"
              :key="gasto.id"
              :class="{ 'is-editing': gasto.editando }"
            >
              <td>
                <input
                  v-if="gasto.editando"
                  v-model="gasto.temp.description"
                  placeholder="Descrição"
                />
                <span v-else>{{ gasto.description }}</span>
              </td>
              <td>
                <select v-if="gasto.editando" v-model="gasto.temp.category">
                  <option disabled value="">Selecione...</option>
                  <option v-for="cat in store.categories" :key="cat.id" :value="cat.name">
                    {{ cat.name }}
                  </option>
                </select>
                <span v-else class="cat-tag">{{ gasto.category }}</span>
              </td>
              <td class="price-cell">
                <input
                  v-if="gasto.editando"
                  type="number"
                  step="0.01"
                  v-model="gasto.temp.amount"
                />
                <span v-else>R$ {{ gasto.amount.toFixed(2) }}</span>
              </td>
              <td>
                <input v-if="gasto.editando" type="date" v-model="gasto.temp.date" />
                <span v-else>{{ new Date(gasto.date).toLocaleDateString("pt-BR") }}</span>
              </td>
              <td class="actions-cell text-center">
                <template v-if="gasto.editando">
                  <button @click="salvarGasto(gasto)" class="btn-icon save" title="Salvar">
                    ✓
                  </button>
                  <button @click="gasto.editando = false" class="btn-icon cancel" title="Cancelar">
                    ✖
                  </button>
                </template>
                <template v-else>
                  <button @click="iniciarEdicaoGasto(gasto)" class="btn-icon edit" title="Editar">
                    ✏️
                  </button>
                  <button @click="removerGasto(gasto.id)" class="btn-icon delete" title="Excluir">
                    🗑️
                  </button>
                </template>
              </td>
            </tr>
            <tr v-if="gastosPessoa.length === 0">
              <td colspan="5" class="text-center" style="padding: 40px; color: #94a3b8">
                Nenhum gasto registrado para esta pessoa.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
    <div v-else class="empty-state">
      <p>Selecione ou adicione uma pessoa para gerenciar os gastos.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useFinanceStore } from "../stores/finance";
import api from "../api/index.js";

const store = useFinanceStore();
const novaPessoa = ref("");
const pessoas = ref([]);
const abaAtiva = ref(null);
const gastosPessoa = ref([]);
const editandoAbaId = ref(null);

const vFocus = { mounted: (el) => el.focus() };

const totalGasto = computed(() => {
  return gastosPessoa.value.reduce((acc, g) => acc + (Number(g.amount) || 0), 0);
});

const carregarDados = async () => {
  try {
    // Garante que as categorias existam na store para o mapeamento de ID
    await store.fetchInitialData();

    // Busca as pessoas (com a barra final exigida pelo main.py)
    const res = await api.get("/people/");
    pessoas.value = res.data;

    if (pessoas.value.length > 0) {
      selecionarPessoa(pessoas.value[0]);
    }
  } catch (error) {
    console.error("Erro ao carregar dados:", error);
  }
};

const selecionarPessoa = async (p) => {
  abaAtiva.value = p;
  // Como o schema Person já traz purchases, usamos os dados locais
  if (p.purchases) {
    gastosPessoa.value = p.purchases.map((g) => ({
      ...g,
      editando: false,
      temp: {},
      // Adicionamos o nome da categoria para exibição na tabela baseada no ID
      category: store.categories.find((c) => c.id === g.category_id)?.name || "Sem Categoria",
    }));
  } else {
    gastosPessoa.value = [];
  }
};

const salvarGasto = async (g) => {
  const person_id = abaAtiva.value.id;

  // Busca o objeto da categoria para pegar o ID numérico
  const categoriaObj = store.categories.find((c) => c.name === g.temp.category);

  if (!categoriaObj) {
    alert("Por favor, selecione uma categoria.");
    return;
  }

  // Prepara o payload EXATAMENTE como o CardPurchaseBase do schemas.py exige
  const payload = {
    description: g.temp.description,
    amount: parseFloat(g.temp.amount), // Converte para float
    date: g.temp.date, // Formato YYYY-MM-DD
    category_id: categoriaObj.id, // ENVIA O ID (INT), NÃO O NOME
  };

  try {
    if (String(g.id).startsWith("new-")) {
      // POST /people/{person_id}/purchases/ conforme main.py
      const res = await api.post(`/people/${person_id}/purchases/`, payload);
      Object.assign(g, { ...res.data, category: categoriaObj.name, editando: false });
    }
  } catch (error) {
    console.error("Erro 422 detalhado:", error.response?.data);
    alert("Erro ao salvar: Verifique se todos os campos estão preenchidos corretamente.");
  }
};

const criarAba = async () => {
  if (!novaPessoa.value.trim()) return;
  try {
    const res = await api.post("/people", { name: novaPessoa.value });
    pessoas.value.push(res.data);
    novaPessoa.value = "";
    selecionarPessoa(res.data);
  } catch (error) {
    console.error("Erro ao criar pessoa:", error);
    alert("Erro ao criar pessoa.");
  }
};

const deletarPessoa = async (id) => {
  if (confirm("Deseja excluir esta aba e todos os seus lançamentos?")) {
    try {
      await api.delete(`/people/${id}`);
      pessoas.value = pessoas.value.filter((p) => p.id !== id);
      if (abaAtiva.value?.id === id) {
        abaAtiva.value = pessoas.value[0] || null;
        if (abaAtiva.value) selecionarPessoa(abaAtiva.value);
      }
    } catch (error) {
      console.error("Erro ao excluir aba:", error);
      alert("Erro ao excluir aba.");
    }
  }
};

const iniciarEdicaoAba = (p) => (editandoAbaId.value = p.id);

const salvarNomeAba = async (pessoa) => {
  if (!pessoa.name.trim()) return carregarDados();
  try {
    await api.put(`/people/${pessoa.id}`, { name: pessoa.name });
    editandoAbaId.value = null;
  } catch (error) {
    console.error("Erro ao renomear:", error);
    alert("Erro ao renomear.");
    carregarDados();
  }
};

const iniciarEdicaoGasto = (g) => {
  g.temp = { ...g };
  g.editando = true;
};

const adicionarLinhaGasto = () => {
  const novaLinha = {
    id: "new-" + Date.now(),
    description: "",
    amount: 0,
    category: store.categories[0]?.name || "Outros",
    date: new Date().toISOString().split("T")[0],
    editando: true,
    temp: {
      description: "",
      amount: 0,
      category: store.categories[0]?.name || "Outros",
      date: new Date().toISOString().split("T")[0],
    },
  };
  gastosPessoa.value.unshift(novaLinha);
};

const removerGasto = async (id) => {
  if (confirm("Deseja excluir este lançamento?")) {
    try {
      // Rota do main.py: @app.delete("/purchases/{purchase_id}")
      await api.delete(`/purchases/${id}`);
      gastosPessoa.value = gastosPessoa.value.filter((g) => g.id !== id);
    } catch (error) {
      console.error("Erro ao excluir:", error);
    }
  }
};

onMounted(carregarDados);
</script>

<style scoped>
/* Preservando e limpando os estilos originais */
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: "Inter", sans-serif;
  color: #1e293b;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}
h1 {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
}
.subtitle {
  color: #64748b;
  margin: 5px 0 0;
}
.add-person-box {
  display: flex;
  gap: 10px;
}
.add-person-box input {
  border: 1px solid #e2e8f0;
  padding: 10px 15px;
  border-radius: 8px;
  width: 220px;
  outline: none;
}
.add-person-box input:focus {
  border-color: #3b82f6;
}
.btn-add {
  background: #1e293b;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.tabs-nav {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 15px;
  flex-wrap: wrap;
}
.tab-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: #f1f5f9;
  border-radius: 20px;
  cursor: pointer;
  color: #64748b;
  font-weight: 500;
  transition: 0.2s;
  border: 1px solid transparent;
}
.tab-pill:hover {
  background: #e2e8f0;
}
.tab-pill.active {
  background: #3b82f6;
  color: white;
  border-color: #2563eb;
}

.input-tab-edit {
  background: transparent;
  border: none;
  color: white;
  width: 80px;
  outline: none;
  font-weight: bold;
  border-bottom: 1px solid white;
}
.btn-remove-tab {
  border: none;
  background: transparent;
  color: inherit;
  font-size: 1.2rem;
  cursor: pointer;
  opacity: 0.6;
  line-height: 1;
}
.btn-remove-tab:hover {
  opacity: 1;
  color: #ef4444;
}

.table-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.card-header {
  padding: 20px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.total-badge {
  background: #dcfce7;
  color: #166534;
  padding: 6px 14px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.9rem;
}
.btn-new-entry {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
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
  padding: 15px 25px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  background: white;
}
td {
  padding: 15px 25px;
  border-top: 1px solid #f1f5f9;
  vertical-align: middle;
}
.text-center {
  text-align: center;
}
.cat-tag {
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  color: #475569;
}
.price-cell {
  font-weight: 700;
  color: #0f172a;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 8px;
  border-radius: 6px;
  transition: 0.2s;
}
.btn-icon:hover {
  background: #f1f5f9;
}
.btn-icon.save {
  color: #10b981;
}
.btn-icon.delete {
  color: #ef4444;
}

.is-editing td {
  background: #fffbeb;
}
.empty-state {
  text-align: center;
  padding: 60px;
  color: #94a3b8;
}

input[type="text"],
input[type="number"],
select,
input[type="date"] {
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  padding: 6px 10px;
  width: 100%;
  outline: none;
  font-size: 0.9rem;
}
input:focus,
select:focus {
  border-color: #3b82f6;
}
</style>
