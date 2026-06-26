<!-- src/views/admin/UsersView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">👤 Gestion des utilisateurs</h1>
        <p class="text-gray-500 text-sm">Gérez tous les comptes utilisateurs</p>
      </div>
    </div>

    <!-- Filtres -->
    <div class="bg-white rounded-xl p-4 shadow-sm border border-purple-100">
      <div class="flex flex-wrap gap-3">
        <input v-model="searchQuery" type="text" placeholder=" Rechercher..." class="flex-1 min-w-[200px] px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400" />
        <select v-model="selectedRole" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400">
          <option value="all">Tous les rôles</option>
          <option value="ADMIN">Admin</option>
          <option value="SOIGNANT">Médecin</option>
          <option value="PATIENTE">Patient</option>
        </select>
        <select v-model="selectedStatus" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400">
          <option value="all">Tous les statuts</option>
          <option value="ACTIVE"> Actif</option>
          <option value="PENDING"> En attente</option>
          <option value="REJECTED"> Rejeté</option>
          <option value="SUSPENDED">Suspendu</option>
        </select>
        <button @click="resetFilters" class="px-4 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition text-sm">Réinitialiser</button>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-purple-100">
      <Loader2 class="w-12 h-12 text-purple-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des utilisateurs...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Tableau -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-purple-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-purple-50 border-b border-purple-100">
            <tr>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Utilisateur</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Email</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Rôle</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Statut</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Inscrit le</th>
              <th class="text-center py-3 px-4 text-xs font-semibold text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-bold">
                    {{ getInitials(user.username) }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-800">{{ user.username }}</p>
                    <p class="text-xs text-gray-500">ID: #{{ user.id }}</p>
                  </div>
                </div>
              </td>
              <td class="py-3 px-4 text-sm text-gray-600">{{ user.email }}</td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 rounded-full text-xs font-medium" :class="user.role === 'ADMIN' ? 'bg-purple-100 text-purple-700' : user.role === 'SOIGNANT' ? 'bg-blue-100 text-blue-700' : 'bg-rose-100 text-rose-700'">
                  {{ user.role }}
                </span>
              </td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getStatusClass(user.account_status)">
                  {{ getStatusLabel(user.account_status) }}
                </span>
              </td>
              <td class="py-3 px-4 text-sm text-gray-500">{{ formatDate(user.created_at) }}</td>
              <td class="py-3 px-4 text-center">
                <div class="flex items-center justify-center gap-1">
                  <button v-if="user.role === 'SOIGNANT' && user.account_status === 'PENDING'" 
                          @click="validateUser(user.id)" 
                          class="p-1.5 rounded-lg hover:bg-green-100 transition text-green-500" title="Valider">
                    <CheckCircle class="w-4 h-4" />
                  </button>
                  <button v-if="user.role === 'SOIGNANT' && user.account_status === 'PENDING'" 
                          @click="rejectUser(user.id)" 
                          class="p-1.5 rounded-lg hover:bg-red-100 transition text-red-500" title="Rejeter">
                    <XCircle class="w-4 h-4" />
                  </button>
                  <button v-if="user.account_status === 'ACTIVE'" 
                          @click="toggleStatus(user.id)" 
                          class="p-1.5 rounded-lg hover:bg-orange-100 transition text-orange-500" title="Suspendre">
                    <ToggleLeft class="w-4 h-4" />
                  </button>
                  <button v-else-if="user.account_status === 'SUSPENDED'" 
                          @click="toggleStatus(user.id)" 
                          class="p-1.5 rounded-lg hover:bg-green-100 transition text-green-500" title="Activer">
                    <ToggleRight class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="filteredUsers.length === 0" class="p-8 text-center">
        <Users class="w-12 h-12 text-gray-300 mx-auto mb-2" />
        <p class="text-gray-500">Aucun utilisateur trouvé</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { ToggleLeft, ToggleRight, Users, CheckCircle, XCircle, Loader2 } from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'AdminUsersView',
  components: { ToggleLeft, ToggleRight, Users, CheckCircle, XCircle, Loader2 },
  setup() {
    const searchQuery = ref('');
    const selectedRole = ref('all');
    const selectedStatus = ref('all');
    const users = ref([]);
    const loading = ref(true);
    const error = ref('');

    const filteredUsers = computed(() => {
      let result = users.value;
      
      if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(u => 
          u.username.toLowerCase().includes(q) || 
          u.email.toLowerCase().includes(q)
        );
      }
      
      if (selectedRole.value !== 'all') {
        result = result.filter(u => u.role === selectedRole.value);
      }
      
      if (selectedStatus.value !== 'all') {
        result = result.filter(u => u.account_status === selectedStatus.value);
      }
      
      return result;
    });

    const getStatusClass = (status) => {
      const classes = {
        'ACTIVE': 'bg-green-100 text-green-700',
        'PENDING': 'bg-yellow-100 text-yellow-700',
        'REJECTED': 'bg-red-100 text-red-700',
        'SUSPENDED': 'bg-gray-100 text-gray-700'
      };
      return classes[status] || 'bg-gray-100 text-gray-700';
    };

    const getStatusLabel = (status) => {
      const labels = {
        'ACTIVE': ' Actif',
        'PENDING': ' En attente',
        'REJECTED': ' Rejeté',
        'SUSPENDED': ' Suspendu'
      };
      return labels[status] || status;
    };

    const resetFilters = () => {
      searchQuery.value = '';
      selectedRole.value = 'all';
      selectedStatus.value = 'all';
    };

    const validateUser = async (id) => {
      if (!confirm('Valider ce compte médecin ?')) return;
      try {
        await api.post(`/admin/users/${id}/validate`);
        const user = users.value.find(u => u.id === id);
        if (user) user.account_status = 'ACTIVE';
        alert(' Compte validé avec succès !');
      } catch (err) {
        console.error(' Erreur validation:', err);
        alert(' Erreur lors de la validation');
      }
    };

    const rejectUser = async (id) => {
      const reason = prompt('Motif du rejet :');
      if (reason === null) return;
      try {
        await api.post(`/admin/users/${id}/reject`, { reason });
        const user = users.value.find(u => u.id === id);
        if (user) {
          user.account_status = 'REJECTED';
          user.rejection_reason = reason;
        }
        alert(' Compte rejeté');
      } catch (err) {
        console.error(' Erreur rejet:', err);
        alert(' Erreur lors du rejet');
      }
    };

    const toggleStatus = async (id) => {
      const user = users.value.find(u => u.id === id);
      if (!user) return;
      
      const newStatus = user.account_status === 'ACTIVE' ? 'SUSPENDED' : 'ACTIVE';
      const action = newStatus === 'ACTIVE' ? 'activer' : 'suspendre';
      
      if (!confirm(`${action.charAt(0).toUpperCase() + action.slice(1)} ce compte ?`)) return;
      
      try {
        await api.put(`/admin/users/${id}/status`, { status: newStatus });
        user.account_status = newStatus;
        alert(` Compte ${action} avec succès`);
      } catch (err) {
        console.error(' Erreur:', err);
        alert(` Erreur lors de la ${action}`);
      }
    };

    const loadUsers = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await api.get('/admin/users');
        console.log(' Utilisateurs:', response.data);
        
        if (response.data && response.data.data) {
          users.value = response.data.data;
        }
      } catch (err) {
        console.error(' Erreur chargement utilisateurs:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadUsers();
    });

    return { 
      users, 
      filteredUsers, 
      searchQuery, 
      selectedRole, 
      selectedStatus,
      loading,
      error,
      formatDate,
      getInitials,
      getStatusClass,
      getStatusLabel,
      resetFilters,
      validateUser,
      rejectUser,
      toggleStatus
    };
  }
};
</script>