<!-- src/views/admin/DashboardView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Administration</h1>
      <p class="text-gray-500 text-sm">Gestion complète de la plateforme</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-purple-100">
      <Loader2 class="w-12 h-12 text-purple-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des statistiques...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Statistiques -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-xl p-4 shadow-sm border border-purple-100">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-purple-500 text-xs font-medium">Utilisateurs</p>
            <p class="text-2xl font-bold text-gray-800">{{ getTotalUsers }}</p>
          </div>
          <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <Users class="w-5 h-5 text-purple-500" />
          </div>
        </div>
        <div class="text-xs text-gray-500 mt-1">
          {{ getPatients }} patients • {{ getCaregivers }} médecins
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm border border-green-100">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-500 text-xs font-medium">Grossesses</p>
            <p class="text-2xl font-bold text-gray-800">{{ getTotalPregnancies }}</p>
          </div>
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <Baby class="w-5 h-5 text-green-500" />
          </div>
        </div>
        <div class="text-xs text-gray-500 mt-1">{{ getActivePregnancies }} actives</div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm border border-blue-100">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-500 text-xs font-medium">Rendez-vous</p>
            <p class="text-2xl font-bold text-gray-800">{{ getTotalAppointments }}</p>
          </div>
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <Calendar class="w-5 h-5 text-blue-500" />
          </div>
        </div>
        <div class="text-xs text-gray-500 mt-1">{{ getPendingAppointments }} en attente</div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm border border-amber-100">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-amber-500 text-xs font-medium">Alertes</p>
            <p class="text-2xl font-bold text-amber-500">{{ getActiveAlerts }}</p>
          </div>
          <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
            <AlertCircle class="w-5 h-5 text-amber-500" />
          </div>
        </div>
        <div class="text-xs text-gray-500 mt-1">{{ getCriticalAlerts }} critiques</div>
      </div>
    </div>

    <!-- Actions rapides -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      <router-link to="/app/admin/users" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-purple-100">
        <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
          <UserCog class="w-6 h-6 text-purple-500" />
        </div>
        <p class="text-sm font-medium text-gray-700">Gérer les utilisateurs</p>
      </router-link>
      <router-link to="/app/admin/stats" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-purple-100">
        <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
          <Activity class="w-6 h-6 text-blue-500" />
        </div>
        <p class="text-sm font-medium text-gray-700">Statistiques</p>
      </router-link>
      <router-link to="/app/admin/logs" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-purple-100">
        <div class="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-2">
          <FileText class="w-6 h-6 text-amber-500" />
        </div>
        <p class="text-sm font-medium text-gray-700">Logs</p>
      </router-link>
      <router-link to="/app/admin/settings" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-purple-100">
        <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
          <Settings class="w-6 h-6 text-purple-500" />
        </div>
        <p class="text-sm font-medium text-gray-700">Paramètres</p>
      </router-link>
    </div>

    <!-- Derniers utilisateurs -->
    <div class="bg-white rounded-xl shadow-sm border border-purple-100 overflow-hidden">
      <div class="px-6 py-4 border-b border-purple-50 flex justify-between items-center">
        <h3 class="font-semibold text-gray-800"> Derniers utilisateurs inscrits</h3>
        <router-link to="/app/admin/users" class="text-purple-500 text-sm hover:underline">Voir tout</router-link>
      </div>
      
      <div v-if="recentUsers.length > 0" class="divide-y divide-purple-50">
        <div v-for="user in recentUsers" :key="user.id" class="px-6 py-3 flex flex-wrap items-center justify-between hover:bg-purple-50/50 transition">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-bold">
              {{ getInitials(user.username) }}
            </div>
            <div>
              <p class="font-medium text-gray-800">{{ user.username }}</p>
              <p class="text-sm text-gray-500">{{ user.email }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="user.role === 'ADMIN' ? 'bg-purple-100 text-purple-700' : user.role === 'SOIGNANT' ? 'bg-blue-100 text-blue-700' : 'bg-rose-100 text-rose-700'">
              {{ user.role }}
            </span>
            <span class="text-sm text-gray-400">{{ formatDate(user.created_at) }}</span>
          </div>
        </div>
      </div>
      <div v-else class="p-8 text-center text-gray-500">Aucun utilisateur récent</div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { 
  Users, Baby, Calendar, UserCog, Activity, Settings, FileText, 
  AlertCircle, Loader2 
} from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'AdminDashboardView',
  components: { 
    Users, Baby, Calendar, UserCog, Activity, Settings, FileText, 
    AlertCircle, Loader2 
  },
  setup() {
    const loading = ref(true);
    const error = ref('');
    const stats = ref({});
    const recentUsers = ref([]);

    // ===== COMPUTED POUR ACCÉDER AUX DONNÉES AVEC LA STRUCTURE DE L'API =====
    
    // Utilisateurs
    const getTotalUsers = computed(() => {
      return stats.value?.users?.total || stats.value?.total_users || 0;
    });
    
    const getPatients = computed(() => {
      return stats.value?.users?.patients || stats.value?.patients || 0;
    });
    
    const getCaregivers = computed(() => {
      return stats.value?.users?.caregivers || stats.value?.caregivers || 0;
    });
    
    // Grossesses
    const getTotalPregnancies = computed(() => {
      return stats.value?.pregnancies?.total || stats.value?.total_pregnancies || 0;
    });
    
    const getActivePregnancies = computed(() => {
      return stats.value?.pregnancies?.active || stats.value?.active_pregnancies || 0;
    });
    
    // Rendez-vous
    const getTotalAppointments = computed(() => {
      return stats.value?.appointments?.total || stats.value?.total_appointments || 0;
    });
    
    const getPendingAppointments = computed(() => {
      return stats.value?.appointments?.pending || stats.value?.pending_appointments || 0;
    });
    
    // Alertes
    const getActiveAlerts = computed(() => {
      return stats.value?.alerts?.active || stats.value?.active_alerts || 0;
    });
    
    const getCriticalAlerts = computed(() => {
      return stats.value?.alerts?.critical || stats.value?.critical_alerts || 0;
    });

    const loadDashboard = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log('📤 Appel API /admin/stats...');
        const response = await api.get('/admin/stats');
        console.log(' Réponse brute:', response.data);
        
        if (response.data) {
          // Structure de l'API : response.data.data
          if (response.data.data) {
            stats.value = response.data.data;
            console.log(' Données extraites de data:', stats.value);
          } 
          // Fallback si les données sont directement dans response.data
          else if (response.data.users) {
            stats.value = response.data;
            console.log(' Données extraites directement:', stats.value);
          }
        }
        
        // Charger les derniers utilisateurs
        try {
          const usersRes = await api.get('/admin/users?limit=5');
          console.log(' Derniers utilisateurs:', usersRes.data);
          
          if (usersRes.data && usersRes.data.data) {
            recentUsers.value = usersRes.data.data.slice(0, 5);
          } else if (Array.isArray(usersRes.data)) {
            recentUsers.value = usersRes.data.slice(0, 5);
          }
        } catch (err) {
          console.warn(' Erreur chargement utilisateurs récents:', err);
        }
        
      } catch (err) {
        console.error(' Erreur chargement dashboard:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadDashboard();
    });

    return {
      loading,
      error,
      stats,
      recentUsers,
      // Computed
      getTotalUsers,
      getPatients,
      getCaregivers,
      getTotalPregnancies,
      getActivePregnancies,
      getTotalAppointments,
      getPendingAppointments,
      getActiveAlerts,
      getCriticalAlerts,
      // Helpers
      formatDate,
      getInitials
    };
  }
};
</script>