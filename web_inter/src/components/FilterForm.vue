<template>
  <form @submit.prevent="applyFilters" class="filter-form">
    <label for="id_user">ИД пользователя:</label>
    <input type="text" v-model="localFilters.id_user" id="id_user" class="filter-input">

    <label for="diagnosis">Диагноз:</label>
    <select v-model="localFilters.diagnosis" id="diagnosis" class="filter-input">
      <option value="">Все</option>
      <option v-for="diagnosis in diagnoses" :key="diagnosis.id" :value="diagnosis.name">
        {{ diagnosis.name }}
      </option>
    </select>

    <label for="start_date">Начальная дата:</label>
    <input type="date" v-model="localFilters.start_date" id="start_date" class="filter-input">

    <label for="end_date">Дата окончания:</label>
    <input type="date" v-model="localFilters.end_date" id="end_date" class="filter-input">

    <button type="submit" class="filter-button">Применить фильтры</button>
  </form>
</template>

<script>
import axios from 'axios';
import { getDiagnoses } from '@/store/diag';

export default {
  name: 'FilterForm',
  props: {
    filters: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      localFilters: { ...this.filters }, // Локальная копия фильтров
      diagnoses: [], // Список диагнозов
    };
  },
  methods: {
    applyFilters() {
      this.$emit('applyFilters', this.localFilters); // Отправка фильтров в родительский компонент
    },
    
  },
  watch: {
    localFilters: {
      handler(newFilters) {
        this.$emit('update:filters', newFilters); // Двусторонняя привязка
      },
      deep: true,
    },
  },
  mounted() {
    this.diagnoses = getDiagnoses();
  },
};
</script>

<style src="../assets/table.css">
</style>