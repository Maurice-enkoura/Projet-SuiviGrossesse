<!-- src/views/doctor/AppointmentsView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Gestion des rendez-vous</h1>
        <p class="text-gray-500 text-sm">Gérez tous les rendez-vous</p>
      </div>
    </div>

    <!-- Filtres -->
    <div class="flex flex-wrap gap-2">
      <button 
        v-for="filter in filters" 
        :key="filter.value" 
        @click="activeFilter = filter.value" 
        class="px-4 py-2 rounded-lg text-sm transition" 
        :class="activeFilter === filter.value ? 'bg-blue-500 text-white' : 'bg-white text-gray-600 hover:bg-blue-50 border border-blue-100'"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des rendez-vous...</p>
    </div>

    <!-- Liste -->
    <div v-else-if="filteredAppointments.length > 0" class="space-y-3">
      <div v-for="appt in filteredAppointments" :key="appt.id" class="bg-white rounded-xl p-4 shadow-sm border border-blue-100 hover:shadow-md transition">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-full flex items-center justify-center text-white" :class="getStatusColor(appt.status)">
              <component :is="getStatusIcon(appt.status)" class="w-5 h-5" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ appt.patient_name || 'Patiente' }}</h3>
              <p class="text-sm text-gray-500">{{ appt.reason || 'Consultation' }}</p>
              <div class="flex flex-wrap items-center gap-3 mt-1 text-sm text-gray-600">
                <span><Calendar class="w-4 h-4 inline mr-1" /> {{ formatDate(appt.date_time) }}</span>
                <span><Clock class="w-4 h-4 inline mr-1" /> {{ formatTime(appt.date_time) }}</span>
                <span class="text-gray-400">{{ appt.duration_minutes || 30 }} min</span>
              </div>
            </div>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <span class="px-3 py-1 rounded-full text-xs font-medium" :class="getStatusBadge(appt.status)">
              {{ getStatusLabel(appt.status) }}
            </span>
            <button 
              v-if="appt.status === 'SCHEDULED'" 
              @click="updateStatus(appt.id, 'CONFIRMED')" 
              class="text-green-500 hover:text-green-700 text-sm px-2 py-1 rounded hover:bg-green-50 transition"
            >
              Confirmer
            </button>
            <button 
              v-if="appt.status === 'CONFIRMED'" 
              @click="updateStatus(appt.id, 'COMPLETED')" 
              class="text-purple-500 hover:text-purple-700 text-sm px-2 py-1 rounded hover:bg-purple-50 transition"
            >
              Terminer
            </button>
            <button 
              v-if="appt.status !== 'CANCELLED' && appt.status !== 'COMPLETED'" 
              @click="updateStatus(appt.id, 'CANCELLED')" 
              class="text-red-500 hover:text-red-700 text-sm px-2 py-1 rounded hover:bg-red-50 transition"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Message vide -->
    <div v-else class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Calendar class="w-16 h-16 text-blue-300 mx-auto mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucun rendez-vous</h3>
      <p class="text-gray-500">Aucun rendez-vous trouvé pour les critères sélectionnés</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Calendar, Clock, CheckCircle, XCircle, Clock as ClockIcon, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'DoctorAppointmentsView',
  components: { Calendar, Clock, CheckCircle, XCircle, ClockIcon, Loader2 },
  setup() {
    const activeFilter = ref('all');
    const appointments = ref([]);
    const loading = ref(true);
    const error = ref('');

    const filters = [
      { label: ' Tous', value: 'all' },
      { label: ' Programmé', value: 'SCHEDULED' },
      { label: ' Confirmé', value: 'CONFIRMED' },
      { label: ' Effectué', value: 'COMPLETED' },
      { label: ' Annulé', value: 'CANCELLED' }
    ];

    const filteredAppointments = computed(() => {
      if (activeFilter.value === 'all') return appointments.value;
      return appointments.value.filter(a => a.status === activeFilter.value);
    });

    const formatTime = (dateTime) => {
      if (!dateTime) return '-';
      try {
        const d = new Date(dateTime);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '-';
      }
    };

    const getStatusColor = (status) => {
      const colors = { 
        'SCHEDULED': 'bg-blue-500', 
        'CONFIRMED': 'bg-green-500', 
        'COMPLETED': 'bg-purple-500', 
        'CANCELLED': 'bg-red-500' 
      };
      return colors[status] || 'bg-gray-500';
    };

    const getStatusIcon = (status) => {
      const icons = { 
        'SCHEDULED': 'ClockIcon', 
        'CONFIRMED': 'CheckCircle', 
        'COMPLETED': 'CheckCircle', 
        'CANCELLED': 'XCircle' 
      };
      return icons[status] || 'ClockIcon';
    };

    const getStatusBadge = (status) => {
      const badges = { 
        'SCHEDULED': 'bg-blue-100 text-blue-700', 
        'CONFIRMED': 'bg-green-100 text-green-700', 
        'COMPLETED': 'bg-purple-100 text-purple-700', 
        'CANCELLED': 'bg-red-100 text-red-700' 
      };
      return badges[status] || 'bg-gray-100 text-gray-700';
    };

    const getStatusLabel = (status) => {
      const labels = { 
        'SCHEDULED': 'Programmé', 
        'CONFIRMED': 'Confirmé', 
        'COMPLETED': 'Effectué', 
        'CANCELLED': 'Annulé' 
      };
      return labels[status] || status;
    };

    const updateStatus = async (id, newStatus) => {
      if (!confirm(`Passer ce rendez-vous en "${getStatusLabel(newStatus)}" ?`)) return;
      
      try {
        await api.post(`/caregiver/appointments/${id}/status`, { status: newStatus });
        const appt = appointments.value.find(a => a.id === id);
        if (appt) appt.status = newStatus;
        alert(` Rendez-vous ${getStatusLabel(newStatus).toLowerCase()}`);
      } catch (err) {
        console.error(' Erreur mise à jour:', err);
        alert(' Erreur lors de la mise à jour');
      }
    };

    const loadAppointments = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await api.get('/caregiver/appointments');
        console.log(' Rendez-vous:', response.data);
        
        if (response.data && response.data.data) {
          appointments.value = response.data.data;
        } else if (Array.isArray(response.data)) {
          appointments.value = response.data;
        } else {
          appointments.value = [];
        }
      } catch (err) {
        console.error(' Erreur chargement rendez-vous:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadAppointments();
    });

    return { 
      appointments, 
      filteredAppointments, 
      filters, 
      activeFilter, 
      loading,
      error,
      formatDate, 
      formatTime,
      getStatusColor, 
      getStatusIcon, 
      getStatusBadge, 
      getStatusLabel,
      updateStatus
    };
  }
};
</script>