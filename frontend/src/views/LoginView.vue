<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Entrar no MeuDinheiro</h2>

      <div v-if="errorMessage" class="error-badge">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="seu@email.com"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="********"
            :disabled="loading"
          />
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? "A entrar..." : "Entrar" }}
        </button>
      </form>

      <p class="footer-text">
        Não tem conta? <router-link to="/register">Registe-se aqui</router-link>
      </p>
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
const errorMessage = ref("");

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = ""; // Reseta erro anterior

  try {
    // A action login no finance.js já lida com o token e redirecionamento interno
    // Mas chamamos aqui para garantir o fluxo de feedback
    await store.login(email.value, password.value);

    // Se o login for bem-sucedido, o store.login já redireciona para "/"
    // mas por segurança podemos reforçar aqui:
    router.push("/");
  } catch (error) {
    console.error("Erro ao tentar logar:", error);

    // Captura a mensagem de erro vinda do FastAPI
    if (error.response && error.response.status === 401) {
      errorMessage.value = "E-mail ou senha incorretos.";
    } else {
      errorMessage.value = "Erro ao conectar com o servidor. Tente novamente.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f8fafc;
}
.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.error-badge {
  background-color: #fee2e2;
  color: #ef4444;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 0.9em;
  border: 1px solid #fecaca;
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
}
input:disabled {
  background-color: #f1f5f9;
  cursor: not-allowed;
}
button {
  width: 100%;
  padding: 14px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
}
button:hover:not(:disabled) {
  background: #2980b9;
}
button:disabled {
  background: #94a3b8;
}
.footer-text {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9em;
  color: #64748b;
}
</style>
