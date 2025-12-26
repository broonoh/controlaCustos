<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <h3>Editar Transação</h3>
      <form @submit.prevent="save">
        <div class="field">
          <label>Descrição</label>
          <input v-model="localForm.description" required />
        </div>

        <div class="field">
          <label>Valor</label>
          <input v-model.number="localForm.amount" type="number" step="0.01" required />
        </div>

        <div class="field">
          <label>Categoria</label>
          <select v-model="localForm.category_id" required>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div class="modal-actions">
          <button type="button" @click="$emit('close')" class="btn-cancel">Cancelar</button>
          <button type="submit" class="btn-save">Salvar Alterações</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps(["show", "transaction", "categories"]);
const emit = defineEmits(["close", "save"]);

const localForm = ref({ ...props.transaction });

// Atualiza o formulário interno quando a transação selecionada mudar
watch(
  () => props.transaction,
  (newVal) => {
    localForm.value = { ...newVal };
  },
  { deep: true }
);

const save = () => {
  emit("save", localForm.value);
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}
.field {
  margin-bottom: 15px;
}
.field label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #34495e;
}
.field input,
.field select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
.btn-save {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-cancel {
  background: #ecf0f1;
  color: #7f8c8d;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
