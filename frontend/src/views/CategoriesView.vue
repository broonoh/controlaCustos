<template>
  <div class="app-container">
    <header class="main-header">
      <div class="title-group">
        <h1>⚙️ Gerenciar Categorias</h1>
      </div>
      <router-link to="/" class="btn-back">Voltar para Home</router-link>
    </header>

    <section class="card form-category-card">
      <div class="form-row-inline">
        <input
          v-model="catForm.name"
          placeholder="Nome da categoria (ex: Lazer)"
          class="input-main"
        />
        <input v-model="catForm.color" type="color" class="input-color" />

        <button @click="handleSubmit" class="btn-add" :disabled="loading">
          {{ loading ? "Processando..." : isEditing ? "Salvar Alterações" : "Adicionar Categoria" }}
        </button>

        <button v-if="isEditing" @click="cancelEdit" class="btn-cancel">Cancelar</button>
      </div>
    </section>

    <section class="card list-card">
      <h3>Categorias Ativas</h3>
      <div class="category-grid">
        <div v-for="c in store.categories" :key="c.id" class="category-item">
          <div class="cat-preview">
            <span class="dot" :style="{ backgroundColor: c.color }"></span>
            <strong>{{ c.name }}</strong>
          </div>
          <div class="cat-actions">
            <button @click="startEdit(c)" class="btn-icon" title="Editar">✏️</button>
            <button @click="handleDelete(c.id)" class="btn-icon" title="Excluir">🗑️</button>
          </div>
        </div>

        <div v-if="store.categories.length === 0" class="empty-msg">
          Nenhuma categoria encontrada.
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useFinanceStore } from "../stores/finance";

const store = useFinanceStore();
const loading = ref(false);
const isEditing = ref(false);
const editingId = ref(null);

// Formulário único para as duas ações
const catForm = ref({ name: "", color: "#3498db" });

onMounted(async () => {
  if (store.categories.length === 0) {
    await store.fetchInitialData();
  }
});

// Alterna entre Criar e Editar
const handleSubmit = async () => {
  if (!catForm.value.name) return alert("Digite um nome!");

  loading.value = true;
  try {
    if (isEditing.value) {
      // Chama a action de update (certifique-se de que ela existe na sua store)
      await store.updateCategory(editingId.value, catForm.value);
      isEditing.value = false;
      editingId.value = null;
    } else {
      await store.addCategory(catForm.value);
    }
    catForm.value = { name: "", color: "#3498db" };
  } catch (error) {
    alert("Erro ao processar categoria. Verifique se o backend está rodando.");
  } finally {
    loading.value = false;
  }
};

// Prepara o formulário para edição
const startEdit = (category) => {
  isEditing.value = true;
  editingId.value = category.id;
  catForm.value = { name: category.name, color: category.color };
  window.scrollTo({ top: 0, behavior: "smooth" }); // Move o scroll para o formulário
};

const cancelEdit = () => {
  isEditing.value = false;
  editingId.value = null;
  catForm.value = { name: "", color: "#3498db" };
};

const handleDelete = async (id) => {
  if (
    confirm("Deseja excluir esta categoria? As transações vinculadas poderão ficar sem categoria.")
  ) {
    await store.deleteCategory(id);
  }
};
</script>

<style scoped>
/* ... Mantendo seus estilos anteriores ... */
.app-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.btn-back {
  text-decoration: none;
  color: #64748b;
  font-weight: 600;
}

.form-row-inline {
  display: flex;
  gap: 15px;
  align-items: center;
}
.input-main {
  flex: 1;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}
.input-color {
  width: 60px;
  height: 45px;
  border: none;
  padding: 0;
  cursor: pointer;
  background: none;
}

.btn-add {
  padding: 12px 24px;
  background: #1e293b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: background 0.2s;
}
.btn-add:hover {
  background: #334155;
}

.btn-cancel {
  padding: 12px;
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 20px;
}
.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}
.cat-preview {
  display: flex;
  align-items: center;
  gap: 10px;
}
.dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.cat-actions {
  display: flex;
  gap: 10px;
}
.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 5px;
  border-radius: 4px;
  transition: background 0.2s;
}
.btn-icon:hover {
  background: #f1f5f9;
}

.empty-msg {
  grid-column: 1 / -1;
  text-align: center;
  color: #94a3b8;
  padding: 40px;
}
</style>
