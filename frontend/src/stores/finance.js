import { defineStore } from "pinia";
import api from "../api";
import router from "../router";

export const useFinanceStore = defineStore("finance", {
  state: () => ({
    transactions: [],
    summary: { balance: 0, income: 0, expense: 0 },
    categories: [],
    token: localStorage.getItem("token") || null,
  }),

  actions: {
    // --- TRATAMENTO DE ERRO GLOBAL ---
    handleApiError(error) {
      console.error("Erro na API:", error.response?.data || error.message);
      if (error.response && error.response.status === 401) {
        console.warn("Sessão expirada ou inválida. Redirecionando...");
        this.logout();
      }
      throw error;
    },

    // --- AUTENTICAÇÃO ---
    async login(email, password) {
      try {
        const formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        const res = await api.post("/token", formData);

        // 1. Salva o token primeiro
        this.token = res.data.access_token;
        localStorage.setItem("token", this.token);
        api.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;

        // 2. BUSCA OS DADOS ANTES DE MUDAR DE PÁGINA
        await this.fetchInitialData();

        // 3. REDIRECIONA APENAS NO FINAL
        router.push("/");
      } catch (error) {
        console.error("Erro no login:", error);
        throw error;
      }
    },

    async register(email, password) {
      try {
        // 1. Cria a conta
        await api.post("/register", { email, password });
        // 2. Tenta logar automaticamente
        await this.login(email, password);
      } catch (error) {
        this.handleApiError(error);
      }
    },

    logout() {
      this.token = null;
      localStorage.removeItem("token");
      delete api.defaults.headers.common["Authorization"];
      this.transactions = [];
      this.categories = [];
      this.summary = { balance: 0, income: 0, expense: 0 };
      router.push("/login");
    },

    // --- BUSCA DE DADOS ---
    async fetchInitialData() {
      if (!this.token) return;

      try {
        const [catRes, transRes, sumRes] = await Promise.all([
          api.get("/categories/"),
          api.get("/transactions/"),
          api.get("/summary/"),
        ]);
        this.categories = catRes.data;
        this.transactions = transRes.data;
        this.summary = sumRes.data;
      } catch (error) {
        this.handleApiError(error);
      }
    },

    // --- CATEGORIAS ---
    async fetchCategories() {
      try {
        const res = await api.get("/categories/");
        this.categories = res.data;
      } catch (e) {
        this.handleApiError(e);
      }
    },

    async addCategory(payload) {
      try {
        await api.post("/categories/", payload);
        await this.fetchCategories();
      } catch (e) {
        this.handleApiError(e);
      }
    },

    // No seu arquivo stores/finance.js dentro de actions:
    async updateCategory(id, categoryData) {
      try {
        const res = await api.put(`/categories/${id}`, categoryData);
        const index = this.categories.findIndex((c) => c.id === id);
        if (index !== -1) {
          this.categories[index] = res.data;
        }
      } catch (error) {
        console.error("Erro ao atualizar categoria", error);
        throw error;
      }
    },

    async deleteCategory(id) {
      try {
        await api.delete(`/categories/${id}`);
        await this.fetchCategories();
      } catch (e) {
        if (e.response?.status === 400) {
          alert("Não é possível excluir: existem transações vinculadas.");
        } else {
          this.handleApiError(e);
        }
      }
    },

    // --- TRANSAÇÕES ---
    async fetchTransactions() {
      try {
        const res = await api.get("/transactions/");
        this.transactions = res.data;
      } catch (e) {
        this.handleApiError(e);
      }
    },

    async fetchSummary() {
      try {
        const res = await api.get("/summary/");
        this.summary = res.data;
      } catch (e) {
        this.handleApiError(e);
      }
    },

    async addTransaction(payload) {
      try {
        await api.post("/transactions/", payload);
        await this.fetchTransactions();
        await this.fetchSummary();
      } catch (e) {
        this.handleApiError(e);
      }
    },

    async updateTransaction(id, payload) {
      try {
        await api.put(`/transactions/${id}`, payload);
        await this.fetchTransactions();
        await this.fetchSummary();
      } catch (e) {
        this.handleApiError(e);
      }
    },

    async deleteTransaction(id) {
      try {
        await api.delete(`/transactions/${id}`);
        await this.fetchTransactions();
        await this.fetchSummary();
      } catch (e) {
        this.handleApiError(e);
      }
    },
  },
});
