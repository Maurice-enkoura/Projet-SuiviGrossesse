<!-- src/views/patient/AppointmentsView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Mes rendez-vous</h1>
        <p class="text-gray-500 text-sm">Gérez vos consultations médicales</p>
      </div>
      <router-link 
        to="/app/patient/appointment/create" 
        class="inline-flex items-center gap-2 px-4 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition"
      >
        <CalendarPlus class="w-4 h-4" /> Prendre rendez-vous
      </router-link>
    </div>

    <!-- Filtres -->
    <div class="flex flex-wrap gap-2">
      <button 
        v-for="filter in filters" 
        :key="filter.value" 
        @click="activeFilter = filter.value" 
        class="px-4 py-2 rounded-lg text-sm transition" 
        :class="activeFilter === filter.value ? 'bg-rose-500 text-white' : 'bg-white text-gray-600 hover:bg-rose-50 border border-rose-100'"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      ❌ {{ error }}
    </div>

    <!-- Liste -->
    <div v-if="!loading && filteredAppointments.length > 0" class="space-y-3">
      <div v-for="appt in filteredAppointments" :key="appt.id" class="bg-white rounded-xl p-4 shadow-sm border border-rose-100 hover:shadow-md transition">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-full flex items-center justify-center text-white" :class="getStatusColor(appt.status)">
              <component :is="getStatusIcon(appt.status)" class="w-5 h-5" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ getDoctorName(appt) }}</h3>
              <p class="text-sm text-gray-500">{{ getSpecialty(appt) }}</p>
              <div class="flex flex-wrap items-center gap-3 mt-1 text-sm text-gray-600">
                <span><Calendar class="w-4 h-4 inline mr-1" /> {{ formatDate(appt.date_time) }}</span>
                <span><Clock class="w-4 h-4 inline mr-1" /> {{ formatTime(appt.date_time) }}</span>
                <span v-if="appt.duration_minutes" class="text-gray-400">{{ appt.duration_minutes }} min</span>
              </div>
              <p v-if="appt.reason" class="text-sm text-gray-500 mt-1">{{ appt.reason }}</p>
            </div>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <span class="px-3 py-1 rounded-full text-xs font-medium" :class="getStatusBadge(appt.status)">
              {{ getStatusLabel(appt.status) }}
            </span>
            <button 
              v-if="appt.status === 'SCHEDULED' || appt.status === 'CONFIRMED'" 
              @click="cancelAppointment(appt.id)" 
              class="text-red-500 hover:text-red-700 text-sm px-3 py-1 rounded-lg hover:bg-red-50 transition"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Chargement -->
    <div v-else-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des rendez-vous...</p>
    </div>

    <!-- Message vide -->
    <div v-else class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Calendar class="w-16 h-16 text-rose-300 mx-auto mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucun rendez-vous</h3>
      <p class="text-gray-500">Prenez votre premier rendez-vous dès maintenant</p>
      <router-link to="/app/patient/appointment/create" class="inline-flex items-center gap-2 mt-4 px-6 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition">
        <CalendarPlus class="w-4 h-4" /> Prendre rendez-vous
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { CalendarPlus, Calendar, Clock, CheckCircle, XCircle, Clock as ClockIcon, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'AppointmentsView',
  components: { CalendarPlus, Calendar, Clock, CheckCircle, XCircle, ClockIcon, Loader2 },
  setup() {
    const activeFilter = ref('all');
    const appointments = ref([]);
    const loading = ref(true);
    const error = ref('');

    const filters = [
      { label: ' Tous', value: 'all' },
      { label: ' À venir', value: 'SCHEDULED' },
      { label: ' Confirmés', value: 'CONFIRMED' },
      { label: ' Effectués', value: 'COMPLETED' },
      { label: ' Annulés', value: 'CANCELLED' }
    ];

    const filteredAppointments = computed(() => {
      if (activeFilter.value === 'all') return appointments.value;
      return appointments.value.filter(a => a.status === activeFilter.value);
    });

    const getDoctorName = (appt) => {
      return appt.caregiver_name || appt.caregiver?.username || appt.doctor || 'Médecin';
    };

    const getSpecialty = (appt) => {
      return appt.specialty || appt.caregiver?.speciality || 'Consultation';
    };

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
        'SCHEDULED': 'Clock', 
        'CONFIRMED': 'CheckCircle', 
        'COMPLETED': 'CheckCircle', 
        'CANCELLED': 'XCircle' 
      };
      return icons[status] || 'Clock';
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

    const cancelAppointment = async (id) => {
      if (!confirm(' Annuler ce rendez-vous ?')) return;
      
      try {
        await api.post(`/patient/appointments/${id}/cancel`);
        const index = appointments.value.findIndex(a => a.id === id);
        if (index !== -1) {
          appointments.value[index].status = 'CANCELLED';
        }
        alert(' Rendez-vous annulé avec succès');
      } catch (error) {
        console.error('Erreur annulation:', error);
        alert(' Erreur lors de l\'annulation');
      }
    };

    const loadAppointments = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log('📤 Chargement des rendez-vous...');
        const response = await api.get('/patient/appointments');
        console.log('📥 Réponse brute:', response.data);
        
        if (response.data && response.data.data) {
          appointments.value = Array.isArray(response.data.data) ? response.data.data : [];
          console.log(' Rendez-vous chargés:', appointments.value.length);
        } else if (Array.isArray(response.data)) {
          appointments.value = response.data;
        } else {
          appointments.value = [];
        }
        
      } catch (error) {
        console.error(' Erreur chargement rendez-vous:', error);
        
        if (error.response?.data?.message) {
          error.value = error.response.data.message;
        } else if (error.request) {
          error.value = 'Impossible de contacter le serveur. Vérifiez que le backend est démarré.';
        } else {
          error.value = 'Erreur lors du chargement des rendez-vous';
        }
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
      getDoctorName,
      getSpecialty,
      getStatusColor, 
      getStatusIcon, 
      getStatusBadge, 
      getStatusLabel, 
      cancelAppointment 
    };
  }
};
</script>