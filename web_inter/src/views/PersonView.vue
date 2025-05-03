<template>
  <div>
    <h1>Пользователи</h1>
    <div class="filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск по логину, имени или ид пользователя"
        class="search-input"
      />
      <div class="filter-options">
        <label>
          <input type="checkbox" v-model="showUnconfirmedOnly" />
          Показать только неподтвержденных пользователей
        </label>
      </div>
    </div>

    <table class="user-table">
      <thead>
        <tr>
          <th>ИД</th>
          <th>Логин</th>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Уровень доверия</th>
          <th>Годы опыта</th>
          <th>Дата подтверждения</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="filteredUsers.length === 0">
          <td colspan="8" style="text-align: center;">Пользователи не найдены</td>
        </tr>
        <tr v-for="user in filteredUsers" :key="user.id_user">
          <td>{{ user.id_user }}</td>
          <td>{{ user.login }}</td>
          <td>{{ user.first_name }}</td>
          <td>{{ user.last_name }}</td>
          <td>
            <input
              type="number"
              v-model.number="user.editTrustLevel"
              :min="1"
              :max="5"
              class="trust-level-input"
            />
          </td>
          <td>
            <input
              type="number"
              v-model.number="user.editExperienceYears"
              :min="0"
              class="experience-input"
              :disabled="user.confirment_exp !== null"
            />
          </td>
          <td>{{ user.confirment_exp ? new Date(user.confirment_exp).toLocaleDateString() : 'Не подтвержден' }}</td>
          <td>
            <button @click="updateTrustLevel(user)" class="update-button">
              Изменить доверие
            </button>
            <button 
              v-if="!user.confirment_exp" 
              @click="confirmUser(user)" 
              class="confirm-button"
              :disabled="!user.editExperienceYears"
            >
              Подтвердить
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import API_BASE_URL from '../config/api';

export default {
  data() {
    return {
      users: [],
      searchQuery: "",
      showUnconfirmedOnly: false,
    };
  },
  computed: {
    filteredUsers() {
      let filtered = this.users;

      if (this.showUnconfirmedOnly) {
        filtered = filtered.filter(user => !user.confirment_exp);
      }

      if (this.searchQuery) {
        const searchStr = this.searchQuery.toLowerCase();
        filtered = filtered.filter(user => {
          const id = user.id_user?.toString() || "";
          const login = user.login?.toLowerCase() || "";
          const firstName = user.first_name?.toLowerCase() || "";
          const lastName = user.last_name?.toLowerCase() || "";

          return (
            login.includes(searchStr) ||
            firstName.includes(searchStr) ||
            lastName.includes(searchStr) ||
            id.includes(searchStr)
          );
        });
      }

      return filtered;
    },
  },
  methods: {
    fetchUsers() {
      axios
        .get(`${API_BASE_URL}/api/users`)
        .then((response) => {
          this.users = response.data.map((user) => ({
            ...user,
            editTrustLevel: user.level_trust,
            editExperienceYears: user.experience_year || 0,
          }));
        })
        .catch((error) => {
          console.error("Ошибка запроса пользователей:", error);
        });
    },
    updateTrustLevel(user) {
      const adminId = localStorage.getItem("client");
      if (!adminId) {
        alert("Отсутствует ИД пользователя.");
        return;
      }

      const params = new URLSearchParams({
        id_user: user.id_user,
        id_admin: adminId,
        level_trust: user.editTrustLevel,
      }).toString();

      axios
        .post(`${API_BASE_URL}/api/users?${params}`)
        .then(() => {
          alert("Уровень доверия изменен.");
        })
        .catch((error) => {
          console.error("Ошибка:", error);
        });
    },
    confirmUser(user) {
      const adminId = localStorage.getItem("client");
      if (!adminId) {
        alert("Отсутствует ИД пользователя.");
        return;
      }

      if (!user.editExperienceYears) {
        alert("Пожалуйста, укажите количество лет опыта.");
        return;
      }

      const params = new URLSearchParams({
        id_user: user.id_user,
        id_admin: adminId,
        experience_year: user.editExperienceYears,
      }).toString();

      axios
        .post(`${API_BASE_URL}/api/confirm_user?${params}`)
        .then(() => {
          alert("Пользователь подтвержден.");
          this.fetchUsers(); // Обновляем список пользователей
        })
        .catch((error) => {
          console.error("Ошибка подтверждения пользователя:", error);
        });
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>


<style src="../assets/table.css">
</style>

<style scoped>
.filters {
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
  align-items: center;
}

.filter-options {
  display: flex;
  align-items: center;
  gap: 10px;
}

.experience-input {
  width: 60px;
  padding: 5px;
}

.confirm-button {
  margin-left: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
