<template>
  <div class="main-layout">
    <header class="navbar">
      <div class="nav-container">
        <router-link to="/" class="logo">💰 MeuDinheiro</router-link>

        <nav class="nav-links">
          <template v-if="store.token">
            <router-link to="/" class="nav-link">Início</router-link>
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
/* ATENÇÃO: Removi o "scoped" para que as regras de base
   valham para TODO o sistema (Tabelas, Gráficos, etc).
*/

:root {
  --primary-dark: #1e293b;
  --text-main: #334155;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Inter", sans-serif;
  background-color: #f8fafc;
  color: var(--text-main);
  line-height: 1.5;
  width: 100%;
  overflow-x: hidden;
}

/* Estrutura Principal */
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navbar Responsiva */
.navbar {
  background: var(--primary-dark);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  flex-wrap: wrap; /* Permite quebra de linha no mobile */
}

.nav-links {
  display: flex;
  align-items: center;
}

/* Estilo dos Links */
.logo {
  text-decoration: none;
  color: white;
  font-weight: 800;
  font-size: 1.3rem;
  white-space: nowrap;
}

.nav-link {
  color: #cbd5e1;
  text-decoration: none;
  margin-left: 20px;
  font-weight: 600;
  transition: color 0.2s;
  font-size: 0.95rem;
}

.nav-link:hover,
.router-link-active {
  color: white;
}

.btn-logout {
  background: #ef4444;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 20px;
  padding: 6px 14px;
  border-radius: 6px;
  font-weight: 600;
  transition: background 0.2s;
}

/* --- RESPONSIVIDADE GLOBAL --- */

/* Celulares e Tablets pequenos */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column; /* Logo em cima, links embaixo */
    gap: 15px;
    text-align: center;
  }

  .nav-links {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap; /* Links quebram linha se não couberem */
    gap: 10px;
  }

  .nav-link {
    margin: 0 10px;
    font-size: 0.9rem;
  }

  .btn-logout {
    margin-left: 10px;
    padding: 8px 16px; /* Botão maior para facilitar o toque */
  }
}

/* Regra de Ouro para Tabelas em Todo o Sistema */
.table-container,
.responsive-table {
  width: 100%;
  overflow-x: auto; /* Scroll lateral apenas na tabela */
  -webkit-overflow-scrolling: touch;
  margin-bottom: 1rem;
}

/* Faz com que inputs não estourem o layout no mobile */
input,
select,
textarea {
  max-width: 100%;
}
</style>
