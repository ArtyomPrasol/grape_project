
<template>
  <table class="styled-table">
    <thead>
      <tr>
        <th>ID запроса</th>
        <th>ID пользователя</th>
        <th>Диагноз</th>
        <th>Комментарий</th>
        <th>Дата создания</th>
        <th>Имя файла</th>
        <th>Обработанный файл</th>
        <th>Отправленное изображение</th>
        <th>Обработанное изображение</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in rows" :key="row.id_req">
        <td>{{ row.id_req }}</td>
        <td>{{ row.id_user }}</td>
        <td>{{ row.diagnosis }}</td>
        <td>{{ row.comment }}</td>
        <td>{{ row.date_create }}</td>
        <td>{{ row.file_name }}</td>
        <td>{{ row.file_name_get }}</td>
        <td>
          <a v-if="row.file_url" :href="row.file_url" download target="_blank">
            <img 
              :src="row.file_url" 
              alt="Отправленное изображение" 
              class="image-preview" 
            />
          </a>
          <span v-else>Отсутствует</span>
        </td>
        <td>
          <a v-if="row.file_url_processed" :href="row.file_url_processed" download target="_blank">
            <img 
              :src="row.file_url_processed" 
              alt="Обработанное изображение" 
              class="image-preview" 
            />
          </a>
          <span v-else>Отсутствует</span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    rows: {
      type: Array,
      required: true,
    },
  },
};
</script>


<style src="../assets/table.css"></style>
<style>
.image-preview {
  max-width: 100px;
  max-height: 100px;
  object-fit: cover;
}
</style>