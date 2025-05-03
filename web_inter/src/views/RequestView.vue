<template>
  <div>
    <h1>Запросы пользователей</h1>
    
    <!-- Форма фильтрации -->
    <FilterForm @applyFilters="fetchRequests" :filters.sync="filters" />

    <!-- Таблица данных -->
    <DataTable :rows="requests" />
  </div>
</template>

<script>
import axios from 'axios';
import FilterForm from '@/components/FilterForm.vue';
import DataTable from '@/components/DataTable.vue';
import API_BASE_URL from '../config/api';

export default {
  name: 'RequestsView',
  components: {
    FilterForm,
    DataTable,
  },
  data() {
    return {
      filters: {
        id_user: '',
        diagnosis: '',
        start_date: '',
        end_date: '',
      },
      requests: [],
    };
  },
  methods: {
    async fetchRequests(newFilters) {
      this.filters = newFilters;
      try {
        console.log("Filter: ", this.filters);
        const response = await axios.get(`${API_BASE_URL}/api/requests`, { params: this.filters });
        console.log('Полученные данные:', response.data); // Debug
        this.requests = response.data;
      } catch (error) {
        console.error("Ошибка при получении запросов:", error);
      }
    },
  },
  mounted() {
 },
};
</script>