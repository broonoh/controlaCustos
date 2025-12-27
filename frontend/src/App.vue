<template>
  <div class="main-layout">
    <header class="navbar">
      <div class="nav-container">
        <router-link to="/" class="logo">💰 MeuDinheiro</router-link>

        <nav class="nav-links">
          <template v-if="store.token">
            <router-link to="/" class="nav-link">Início</router-link>
            <router-link to="/cartao" class="nav-link">Terceiros</router-link>
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

    <main class="content-wrapper">
      <router-view />
    </main>
  </div>
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

<style>
/* Estilos Globais (Sem scoped para afetar todo o app) */
:root {
  --primary-dark: #1e293b;
  --bg-light: #f1f5f9;
  --text-main: #334155;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Inter", sans-serif;
  background-color: var(--bg-light);
  color: var(--text-main);
  line-height: 1.5;
  width: 100%;
  overflow-x: hidden; /* Crucial para evitar quebra lateral no celular */
}

.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navbar Adaptável */
.navbar {
  background: var(--primary-dark);
  color: white;
  padding: 0.8rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 15px;
}

.nav-links {
  display: flex;
  align-items: center;
}

.logo {
  text-decoration: none;
  color: white;
  font-weight: 800;
  font-size: 1.2rem;
  white-space: nowrap;
}

.nav-link {
  color: #cbd5e1;
  text-decoration: none;
  margin-left: 15px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: 0.2s;
}

.nav-link:hover,
.router-link-active {
  color: white;
}

/* Área de Conteúdo principal */
.content-wrapper {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 15px; /* Espaçamento interno para não colar nas bordas */
}

.btn-logout {
  background: #ef4444;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 15px;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
}

/* --- MEDIA QUERIES --- */

/* Ajustes para Celulares (Mobile) */
@media (max-width: 640px) {
  .nav-container {
    flex-direction: column;
    gap: 12px;
    padding: 10px;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap; /* Faz os links quebrarem linha se necessário */
    gap: 8px;
  }

  .nav-link {
    margin: 0 5px;
    font-size: 0.85rem;
  }

  .btn-logout {
    margin-left: 5px;
  }

  /* Ajuste para Cards e Gráficos no mobile */
  .dashboard-grid {
    grid-template-columns: 1fr !important; /* Força uma única coluna */
  }
}

/* Utilitários globais para Tabelas (Use nos seus componentes) */
.table-responsive {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  background: white;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}
</style>
