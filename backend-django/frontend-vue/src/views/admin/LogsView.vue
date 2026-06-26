<!-- src/views/admin/LogsView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Logs d'activité</h1>
      <p class="text-gray-500 text-sm">Consultez l'historique des actions</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-purple-100">
      <Loader2 class="w-12 h-12 text-purple-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des logs...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Tableau des logs -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-purple-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-purple-50 border-b border-purple-100">
            <tr>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Date</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Utilisateur</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Action</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id" class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 text-sm text-gray-600">{{ formatDateTime(log.created_at) }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <span class="font-medium text-gray-800">{{ log.user?.username || 'Inconnu' }}</span>
                  <span class="text-xs px-2 py-0.5 rounded-full" :class="log.user?.role === 'ADMIN' ? 'bg-purple-100 text-purple-700' : log.user?.role === 'SOIGNANT' ? 'bg-blue-100 text-blue-700' : 'bg-rose-100 text-rose-700'">
                    {{ log.user?.role || 'N/A' }}
                  </span>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium" :class="getActionClass(log.action)">
                  {{ log.action }}
                </span>
              </td>
              <td class="py-3 px-4 text-sm text-gray-600 max-w-xs truncate" :title="log.description">
                {{ log.description }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="logs.length === 0" class="p-8 text-center">
        <FileText class="w-12 h-12 text-gray-300 mx-auto mb-2" />
        <p class="text-gray-500">Aucun log trouvé</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { FileText, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'AdminLogsView',
  components: { FileText, Loader2 },
  setup() {
    const logs = ref([]);
    const loading = ref(true);
    const error = ref('');

    const formatDateTime = (date) => {
      if (!date) return '-';
      try {
        const d = new Date(date);
        return d.toLocaleString('fr-FR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch {
        return '-';
      }
    };

    const getActionClass = (action) => {
      const classes = {
        'LOGIN': 'bg-green-100 text-green-700',
        'REGISTER': 'bg-blue-100 text-blue-700',
        'CREATE_PREGNANCY': 'bg-rose-100 text-rose-700',
        'CREATE_APPOINTMENT': 'bg-blue-100 text-blue-700',
        'CREATE_ALERT': 'bg-red-100 text-red-700',
        'ADMIN_CREATE_USER': 'bg-purple-100 text-purple-700',
        'ADMIN_DEACTIVATE_USER': 'bg-orange-100 text-orange-700',
        'ADMIN_CHANGE_ROLE': 'bg-purple-100 text-purple-700',
        'LOGOUT': 'bg-gray-100 text-gray-700'
      };
      return classes[action] || 'bg-gray-100 text-gray-700';
    };

    const loadLogs = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await api.get('/admin/logs');
        console.log('📥 Logs:', response.data);
        
        if (response.data && response.data.data) {
          logs.value = response.data.data;
        }
      } catch (err) {
        console.error(' Erreur chargement logs:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadLogs();
    });

    return {
      logs,
      loading,
      error,
      formatDateTime,
      getActionClass
    };
  }
};
</script>