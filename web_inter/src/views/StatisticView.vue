<template>
  <div>
    <h1>Диагнозы и их количество</h1>

    <FilterForm @applyFilters="fetchStatsData" :filters.sync="filters" />

    <DiagnosisChart :statsData="statsData" />
  </div>
</template>

<script>
import axios from "axios";
import API_BASE_URL from '../config/api';
import DiagnosisChart from "../components/ChartDiag.vue";
import FilterForm from "@/components/FilterForm.vue";



export default {
  components: {
    DiagnosisChart,
    FilterForm,
  },
  data() {
    return {
      filters: {
        id_user: '',
        diagnosis: '',
        start_date: '',
        end_date: '',
      },
      statsData: [], // Данные для графика
    };
  },
  mounted() {
  },
  methods: {
    async fetchStatsData(newFilters) {
      this.filters = newFilters;
      try {
        console.log("Filter: ", this.filters);
        const response = await axios.get(`${API_BASE_URL}/api/stats`, {params: this.filters});
        console.log("API Response:", response.data); // Логируем ответ API
        this.statsData = response.data;
      } catch (error) {
        console.error("Ошибка при получении статистики:", error);
      }
    },
  },
};
</script>