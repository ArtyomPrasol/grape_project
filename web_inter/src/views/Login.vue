<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '@/store/auth'; 
import API_BASE_URL from '../config/api';

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMessage = ref('');

const handleLogin = async () => {
  errorMessage.value = '';
  try {
    const response = await fetch(`${API_BASE_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || 'Ошибка входа');
    }

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('client', data.client);
    login();
    router.push('/');
  } catch (error) {
    console.error("Ошибка при входе:", error);
    errorMessage.value = error.message;
  }
};
</script>

<template>
  <div class="login-container">
    <h1>Авторизации</h1>
    <form @submit.prevent="handleLogin">
      <label for="username">Имя пользователя:</label>
      <input id="username" v-model="username" type="text" required />

      <label for="password">Пароль:</label>
      <input id="password" v-model="password" type="password" required />

      <button type="submit">Войти</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<style scoped src="../assets/st.css">

</style>