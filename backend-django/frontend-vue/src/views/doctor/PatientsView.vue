<!-- src/views/doctor/PatientsView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Mes patientes</h1>
        <p class="text-gray-500 text-sm">Liste de toutes vos patientes</p>
      </div>
    </div>

    <!-- Recherche et filtres -->
    <div class="bg-white rounded-xl p-4 shadow-sm border border-blue-100">
      <div class="flex flex-wrap gap-3">
        <input v-model="searchQuery" type="text" placeholder="🔍 Rechercher..." class="flex-1 min-w-[200px] px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" />
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Tableau -->
    <div class="bg-white rounded-xl shadow-sm border border-blue-100 overflow-hidden">
      <div v-if="loading" class="p-12 text-center">
        <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
        <p class="text-gray-500 mt-4">Chargement des patientes...</p>
      </div>
      
      <div v-else-if="filteredPatients.length > 0" class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-blue-50 border-b border-blue-100">
            <tr>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Patiente</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Contact</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Rôle</th>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Inscrite le</th>
              <th class="text-center py-3 px-4 text-xs font-semibold text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in filteredPatients" :key="patient.id" class="border-b border-blue-50 hover:bg-blue-50/50 transition">
              <td class="py-3 px-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                    {{ getInitials(patient.username) }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-800">{{ patient.username }}</p>
                    <p class="text-xs text-gray-500">ID: #{{ patient.id }}</p>
                  </div>
                </div>
              </td>
              <td class="py-3 px-4">
                <p class="text-sm text-gray-600">{{ patient.email }}</p>
                <p class="text-xs text-gray-400">{{ patient.phone || 'Non renseigné' }}</p>
              </td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 rounded-full text-xs font-medium bg-rose-100 text-rose-700">
                  {{ patient.role }}
                </span>
              </td>
              <td class="py-3 px-4 text-sm text-gray-500">{{ formatDate(patient.created_at) }}</td>
              <td class="py-3 px-4 text-center">
                <div class="flex items-center justify-center gap-2">
                  <router-link :to="`/app/doctor/patients/${patient.id}`" class="p-1.5 rounded-lg hover:bg-blue-100 transition text-blue-500" title="Voir">
                    <Eye class="w-4 h-4" />
                  </router-link>
                  <button @click="messagePatient(patient.id)" class="p-1.5 rounded-lg hover:bg-blue-100 transition text-green-500" title="Message">
                    <MessageCircle class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="p-8 text-center">
        <Users class="w-12 h-12 text-gray-300 mx-auto mb-2" />
        <p class="text-gray-500">Aucune patiente trouvée</p>
      </div>

      <div v-if="filteredPatients.length > 0" class="px-4 py-3 border-t border-blue-50 flex flex-wrap items-center justify-between gap-2">
        <p class="text-sm text-gray-500">Total : {{ filteredPatients.length }} patientes</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Eye, MessageCircle, Users, Loader2 } from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'DoctorPatientsView',
  components: { Eye, MessageCircle, Users, Loader2 },
  setup() {
    const searchQuery = ref('');
    const patients = ref([]);
    const loading = ref(true);
    const error = ref('');

    const filteredPatients = computed(() => {
      if (!searchQuery.value) return patients.value;
      const q = searchQuery.value.toLowerCase();
      return patients.value.filter(p => 
        p.username?.toLowerCase().includes(q) || 
        p.email?.toLowerCase().includes(q)
      );
    });

    const messagePatient = (id) => {
      alert(` Envoyer un message à la patiente #${id}`);
    };

    const loadPatients = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await api.get('/caregiver/patients');
        console.log(' Patients:', response.data);
        
        if (response.data && response.data.data) {
          patients.value = response.data.data;
        } else if (Array.isArray(response.data)) {
          patients.value = response.data;
        } else {
          patients.value = [];
        }
      } catch (err) {
        console.error(' Erreur chargement patients:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement des patientes';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadPatients();
    });

    return { 
      patients, 
      filteredPatients, 
      searchQuery,
      loading,
      error,
      formatDate,
      getInitials,
      messagePatient 
    };
  }
};
</script>