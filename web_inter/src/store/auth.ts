import { ref } from 'vue';

// Реактивное состояние авторизации
export const isAuthenticated = ref(!!localStorage.getItem('access_token'));

// Функция для входа
export const login = () => {
  isAuthenticated.value = true;
};

// Функция для выхода
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('client')
  isAuthenticated.value = false;
};