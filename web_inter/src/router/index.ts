import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RequestView from '../views/RequestView.vue'
import PersonView from '../views/PersonView.vue'
import StatisticView from '../views/StatisticView.vue'
import LoginView from '../views/Login.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Основная страница',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'Вход',
      component: LoginView,
    },
    {
      path: '/request',
      name: 'Запросы',
      component: RequestView,
      meta: { requiresAuth: true }, // Требуется авторизация
    },
    {
      path: '/person',
      name: 'Пользователи',
      component: PersonView,
      meta: { requiresAuth: true }, // Требуется авторизация
    },
    {
      path: '/stat',
      name: 'Статистика',
      component: StatisticView,
      meta: { requiresAuth: true }, // Требуется авторизация
    },
  ],
})

// Хук перед каждой навигацией
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token'); // Проверяем наличие токена

  if (to.meta.requiresAuth && !token) {
    // Если маршрут защищён и токена нет, перенаправляем на страницу логина
    next('/login');
  } else {
    // Иначе разрешаем переход
    next();
  }
});

export default router
