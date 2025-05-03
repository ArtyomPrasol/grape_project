<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { ref, computed } from 'vue';
import { isAuthenticated, logout } from './store/auth';
import { fetchDiagnoses } from './store/diag';
import API_BASE_URL from './config/api';

const router = useRouter();
// Глобальное состояние авторизации
fetchDiagnoses();

const handleLogout = () => {
  logout(); // Выход через функцию
  router.push('/login'); // Перенаправляем на страницу входа
};

const downloadArchive = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/export_archive`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error('Ошибка при загрузке архива');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'grape_diagnoses.zip');
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Ошибка при загрузке архива:', error);
    alert('Не удалось скачать архив.');
  }
};

</script>

<template>
  <header>
    <nav class="nav-container">
      <RouterLink 
        to="/" 
        class="nav-link" 
        :class="{ active: $route.path === '/' }">
        Домашняя страница
      </RouterLink>
      <RouterLink 
        to="/request" 
        class="nav-link" 
        :class="{ active: $route.path === '/request' }">
        Запросы
      </RouterLink>
      <RouterLink 
        to="/person" 
        class="nav-link" 
        :class="{ active: $route.path === '/person' }">
        Пользователи
      </RouterLink>
      <RouterLink 
        to="/stat" 
        class="nav-link" 
        :class="{ active: $route.path === '/stat' }">
        Статистика
      </RouterLink>

      <button 
      v-if="isAuthenticated" 
      @click="downloadArchive" 
      class="nav-button">
      Скачать архив
      </button>

      <button v-if="isAuthenticated" 
      @click="handleLogout" 
      class="nav-button">
      Выход
      </button>

      <RouterLink v-else 
      to="/login" 
      class="nav-button">
      Вход
      </RouterLink>

    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style src="./assets/st.css">

</style>
