<template>
  <header class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">💰 MeuDinheiro</router-link>
      <nav>
        <template v-if="store.token">
          <router-link to="/" class="nav-link">Dashboard</router-link>
          <router-link to="/categories" class="nav-link">Categorias</router-link>
          <button @click="handleLogout" class="btn-logout">Sair</button>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link">Entrar</router-link>
          <router-link to="/register" class="nav-link">Cadastrar</router-link>
        </template>
      </nav>
    </div>
  </header>

  <main class="content">
    <router-view />
  </main>
</template>

<script setup>
import { useFinanceStore } from "./stores/finance";
import { useRouter } from "vue-router";

const store = useFinanceStore();
const router = useRouter();

const handleLogout = () => {
  if (confirm("Deseja sair?")) {
    store.logout();
    router.push("/login");
  }
};
</script>

<style scoped>
/* Scoped garante que o CSS não vaze para outros componentes */
.navbar {
  background: #1e293b; /* Cor combinando com sua HomeView */
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
.logo {
  text-decoration: none;
  color: white;
  font-weight: 800;
  font-size: 1.3rem;
}
.nav-link {
  color: #cbd5e1;
  text-decoration: none;
  margin-left: 20px;
  font-weight: 600;
  transition: color 0.2s;
}
.nav-link:hover,
.router-link-active {
  color: white;
}
.content {
  padding: 0; /* Removido para não conflitar com o padding da HomeView */
}
.btn-logout {
  background: #ef4444;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 20px;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
}
.btn-logout:hover {
  background: #dc2626;
}
</style>
