import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
// Nota: Removi os imports estáticos de Dashboard e CategoriesView se você for usá-los como dynamic imports abaixo para economizar memória

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/categories",
      name: "categories",
      component: () => import("../views/CategoriesView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/cartao",
      name: "CardManagement",
      component: () => import("../views/CardManagement.vue"),
      // ADICIONADO: Proteção para garantir que precisa estar logado
      meta: { requiresAuth: true },
    },
  ],
});

// Proteção de Rotas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
