<!-- src/views/doctor/PatientDetailView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div class="flex items-center gap-3">
      <button @click="$router.back()" class="p-2 rounded-lg hover:bg-blue-50 transition">
        <ArrowLeft class="w-5 h-5 text-gray-600" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-800">👤 Détail de la patiente</h1>
        <p class="text-gray-500 text-sm">{{ patient?.username || 'Chargement...' }}</p>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Détails -->
    <div v-else-if="patient" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Informations patiente -->
      <div class="lg:col-span-1 space-y-4">
        <div class="bg-white rounded-xl p-5 shadow-sm border border-blue-100">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
              {{ getInitials(patient.username) }}
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ patient.username }}</h3>
              <p class="text-sm text-gray-500">{{ patient.email }}</p>
              <span class="inline-block mt-1 px-2 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-700">
                {{ patient.role }}
              </span>
            </div>
          </div>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between"><span class="text-gray-500">Téléphone</span><span>{{ patient.phone || 'Non renseigné' }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Date de naissance</span><span>{{ patient.date_of_birth ? formatDate(patient.date_of_birth) : 'Non renseignée' }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Inscrite le</span><span>{{ formatDate(patient.created_at) }}</span></div>
          </div>
        </div>

        <!-- Grossesses -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-blue-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Grossesses</h3>
          <div v-if="pregnancies.length > 0">
            <div v-for="preg in pregnancies" :key="preg.id" class="flex items-center justify-between p-2 hover:bg-blue-50 rounded-lg">
              <div>
                <span class="font-medium">#{{ preg.id }}</span>
                <span class="text-sm text-gray-500 ml-2">Début: {{ formatDate(preg.start_date) }}</span>
              </div>
              <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="preg.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'">
                {{ preg.is_active ? ' Active' : 'Terminée' }}
              </span>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500 text-sm">Aucune grossesse enregistrée</div>
        </div>
      </div>

      <!-- Historique médical -->
      <div class="lg:col-span-2 space-y-4">
        <!-- Rendez-vous -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-blue-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Rendez-vous</h3>
          <div v-if="appointments.length > 0" class="space-y-2">
            <div v-for="appt in appointments" :key="appt.id" class="flex items-center justify-between p-2 bg-blue-50 rounded-lg">
              <div>
                <span class="font-medium">{{ formatDate(appt.date_time) }}</span>
                <span class="text-sm text-gray-500 ml-2">{{ formatTime(appt.date_time) }}</span>
                <p class="text-sm text-gray-600">{{ appt.reason }}</p>
              </div>
              <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="getStatusBadge(appt.status)">
                {{ getStatusLabel(appt.status) }}
              </span>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500 text-sm">Aucun rendez-vous</div>
        </div>

        <!-- Consultations -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-blue-100">
          <h3 class="font-semibold text-gray-800 mb-3">🩺 Consultations</h3>
          <div v-if="consultations.length > 0" class="space-y-2">
            <div v-for="cons in consultations" :key="cons.id" class="p-2 bg-blue-50 rounded-lg">
              <div class="flex items-center justify-between">
                <span class="font-medium">{{ formatDate(cons.consultation_date) }}</span>
                <span class="px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">Terminée</span>
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ cons.report ? cons.report.substring(0, 100) + '...' : 'Aucun rapport' }}</p>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500 text-sm">Aucune consultation</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { ArrowLeft, Loader2 } from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'DoctorPatientDetailView',
  components: { ArrowLeft, Loader2 },
  setup() {
    const route = useRoute();
    const patient = ref(null);
    const pregnancies = ref([]);
    const appointments = ref([]);
    const consultations = ref([]);
    const loading = ref(true);
    const error = ref('');

    const formatTime = (dateTime) => {
      if (!dateTime) return '-';
      try {
        const d = new Date(dateTime);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '-';
      }
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

    const loadPatientData = async () => {
      const id = route.params.id;
      if (!id) {
        error.value = 'ID patient manquant';
        loading.value = false;
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        // Récupérer les infos de la patiente
        const patientRes = await api.get(`/caregiver/patients/${id}`);
        console.log(' Patient:', patientRes.data);
        patient.value = patientRes.data?.patient || patientRes.data;

        // Récupérer les grossesses
        const pregRes = await api.get(`/patient/pregnancies`);
        pregnancies.value = pregRes.data?.data || [];

        // Récupérer les rendez-vous
        const apptRes = await api.get(`/patient/appointments`);
        appointments.value = apptRes.data?.data || [];

        // Récupérer les consultations
        // TODO: Ajouter l'endpoint si disponible

      } catch (err) {
        console.error(' Erreur chargement patient:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadPatientData();
    });

    return {
      patient,
      pregnancies,
      appointments,
      consultations,
      loading,
      error,
      formatDate,
      formatTime,
      getInitials,
      getStatusBadge,
      getStatusLabel
    };
  }
};
</script>