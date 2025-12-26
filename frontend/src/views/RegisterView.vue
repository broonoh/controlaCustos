<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Criar Conta</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="exemplo@email.com"
            :disabled="loading"
          />
        </div>
        <div class="form-group">
          <label>Senha</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="No mínimo 6 caracteres"
            :disabled="loading"
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? "Criando conta..." : "Registrar e Entrar" }}
        </button>
      </form>
      <p class="footer-text">Já tem conta? <router-link to="/login">Faça login</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useFinanceStore } from "../stores/finance";
import { useRouter } from "vue-router";

const store = useFinanceStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);

const handleRegister = async () => {
  // Validação básica de frontend
  if (password.value.length < 6) {
    return alert("A senha deve ter pelo menos 6 caracteres.");
  }

  loading.value = true;

  try {
    console.log("Tentando registrar usuário:", email.value);

    // Chama a action 'register' que agora está no seu finance.js corrigido
    await store.register(email.value, password.value);

    console.log("Registro e login automáticos concluídos com sucesso.");

    // Redireciona para o Dashboard (Home)
    router.push("/");
  } catch (error) {
    console.error("Erro capturado no componente de registro:", error);

    // Tenta extrair a mensagem de erro detalhada do FastAPI
    let errorMessage = "Erro ao conectar com o servidor.";

    if (error.response && error.response.data) {
      // O FastAPI costuma enviar o erro dentro de 'detail'
      errorMessage = error.response.data.detail || JSON.stringify(error.response.data);
    } else if (error.message) {
      errorMessage = error.message;
    }

    alert("Falha no registro: " + errorMessage);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}
.auth-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}
h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}
.form-group {
  margin-bottom: 20px;
}
label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}
input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}
input:focus {
  border-color: #2ecc71;
  outline: none;
}
button {
  width: 100%;
  padding: 14px;
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}
button:hover:not(:disabled) {
  background: #27ae60;
}
button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}
.footer-text {
  text-align: center;
  margin-top: 20px;
}
</style>
