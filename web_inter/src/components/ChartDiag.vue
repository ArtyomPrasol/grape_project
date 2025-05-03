<template>

    <div class="chart-container">
        <canvas id="diagnosis-chart"></canvas>
    </div>

</template>
  
  <script>
import { ref, onMounted, watch } from "vue";
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip,
} from "chart.js";

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Legend,
  Tooltip
);

export default {
  props: {
    statsData: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const chart = ref(null);

    const renderChart = () => {
      const ctx = document.getElementById("diagnosis-chart").getContext("2d");

      const labels = props.statsData.map((item) => item.diagnosis);
      const data = props.statsData.map((item) => item.count);

      if (chart.value) {
        chart.value.destroy(); // Удаляем старый график
      }

      chart.value = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Количество",
              data,
              backgroundColor: [
                "#FF6384",
                "#36A2EB",
                "#FFCE56",
                "#4BC0C0",
                "#9966FF",
                "#FF9F40",
              ],
              borderColor: "#ccc",
              borderWidth: 1,
            },
          ],
        },
        options: {
            responsive: true, // График будет подстраиваться под контейнер
            maintainAspectRatio: false, // Отключаем сохранение пропорций (позволяет использовать фиксированную высоту)
            plugins: {
                legend: {
                    position: "top",
      },
    },
  },
      });
    };

    onMounted(() => {
        console.log("Received statsData:", props.statsData);

        if (!props.statsData || props.statsData.length === 0) {
            console.log("No data available for the chart.");
            return;
        }

        renderChart();
    });

    watch(() => props.statsData, renderChart, { deep: true }); // Отслеживаем изменения props.statsData

    return { chart };
  },
};
  </script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%; /* Ширина контейнера */
  max-width: 800px; /* Максимальная ширина графика */
  margin: 0 auto; /* Центрируем график */
  height: 400px; /* Фиксированная высота графика */
  overflow: hidden; /* Предотвращаем выход элементов за границы */
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}
</style>