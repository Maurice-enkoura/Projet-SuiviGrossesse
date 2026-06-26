<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Consultations</h1>
      <p class="text-gray-500 text-sm">Gérez toutes vos consultations médicales</p>
    </div>

    <!-- Filtres -->
    <div class="bg-white rounded-xl p-4 shadow-sm border border-blue-100">
      <div class="flex flex-wrap gap-3">
        <input v-model="searchQuery" type="text" placeholder=" Rechercher..." class="flex-1 min-w-[200px] px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" />
        <select v-model="selectedFilter" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400">
          <option value="all">Tous</option>
          <option value="SCHEDULED">Programmés</option>
          <option value="CONFIRMED">Confirmés</option>
          <option value="COMPLETED">Terminés</option>
          <option value="CANCELLED">Annulés</option>
        </select>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des consultations...</p>
    </div>

    <!-- Liste -->
    <div v-else-if="filteredConsultations.length > 0" class="space-y-3">
      <div v-for="appt in filteredConsultations" :key="appt.id" class="bg-white rounded-xl p-4 shadow-sm border border-blue-100 hover:shadow-md transition">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold" :class="getStatusColor(appt.status)">
              {{ getInitials(appt.patient_name) }}
            </div>
            <div class="flex-1">
              <div class="flex flex-wrap items-center gap-2">
                <h3 class="font-semibold text-gray-800">{{ appt.patient_name }}</h3>
                <span class="text-xs text-gray-400">#{{ appt.patient_id }}</span>
              </div>
              <p class="text-sm text-gray-500">{{ appt.reason }}</p>
              <div class="flex flex-wrap items-center gap-3 mt-1 text-sm text-gray-600">
                <span> {{ formatDate(appt.date_time) }}</span>
                <span> {{ formatTime(appt.date_time) }}</span>
                <span>⏱ {{ appt.duration_minutes }} min</span>
              </div>
              
              <!-- Constantes vitales -->
              <div v-if="appt.vital_signs" class="mt-2 flex flex-wrap gap-2">
                <span v-if="appt.vital_signs.weight_kg" class="px-2 py-1 bg-blue-50 rounded text-xs">
                   {{ appt.vital_signs.weight_kg }} kg
                </span>
                <span v-if="appt.vital_signs.blood_pressure_systolic" class="px-2 py-1 bg-blue-50 rounded text-xs">
                   {{ appt.vital_signs.blood_pressure_systolic }}/{{ appt.vital_signs.blood_pressure_diastolic }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex flex-wrap items-center gap-2">
            <span class="px-3 py-1 rounded-full text-xs font-medium" :class="getStatusBadge(appt.status)">
              {{ getStatusLabel(appt.status) }}
            </span>
            
            <!-- Boutons d'action -->
            <button v-if="appt.status === 'CONFIRMED'" 
                    @click="startConsultation(appt.id)" 
                    class="px-3 py-1 bg-blue-500 text-white rounded-lg text-xs hover:bg-blue-600 transition">
               Démarrer
            </button>
            
            <button v-if="appt.status === 'COMPLETED' && !appt.has_consultation" 
                    @click="openConsultationModal(appt)" 
                    class="px-3 py-1 bg-purple-500 text-white rounded-lg text-xs hover:bg-purple-600 transition">
               Compte-rendu
            </button>
            
            <button v-if="appt.status === 'COMPLETED'" 
                    @click="viewConsultation(appt.id)" 
                    class="px-3 py-1 bg-green-500 text-white rounded-lg text-xs hover:bg-green-600 transition">
               Voir
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Calendar class="w-16 h-16 text-blue-300 mx-auto mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucune consultation</h3>
      <p class="text-gray-500">Aucune consultation trouvée</p>
    </div>

    <!-- Modal Compte-rendu -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-800"> Compte-rendu de consultation</h2>
          <button @click="showModal = false" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Patiente</label>
            <p class="font-medium">{{ selectedAppointment?.patient_name }}</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Compte-rendu *</label>
            <textarea v-model="consultationReport" rows="6" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" placeholder="Rédigez votre compte-rendu médical..."></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"> Fichiers joints</label>
            <input type="file" multiple @change="handleFileUpload" class="w-full" accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" />
            <p class="text-xs text-gray-400 mt-1">PDF, JPG, PNG, DOC - Max 10MB</p>
          </div>
          
          <div class="flex gap-3 pt-4 border-t">
            <button @click="saveConsultation" class="flex-1 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition" :disabled="saving">
              <Loader2 v-if="saving" class="w-4 h-4 animate-spin inline mr-2" />
              {{ saving ? 'Enregistrement...' : ' Enregistrer' }}
            </button>
            <button @click="showModal = false" class="px-6 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition">Annuler</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Calendar, Loader2 } from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'DoctorConsultationsView',
  components: { Calendar, Loader2 },
  setup() {
    const searchQuery = ref('');
    const selectedFilter = ref('all');
    const appointments = ref([]);
    const loading = ref(true);
    const showModal = ref(false);
    const saving = ref(false);
    const selectedAppointment = ref(null);
    const consultationReport = ref('');
    const uploadedFiles = ref([]);

    const filteredConsultations = computed(() => {
      let result = appointments.value;
      
      if (selectedFilter.value !== 'all') {
        result = result.filter(a => a.status === selectedFilter.value);
      }
      
      if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(a => 
          (a.patient_name || '').toLowerCase().includes(q)
        );
      }
      
      return result;
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
        'SCHEDULED': ' Programmé',
        'CONFIRMED': ' Confirmé',
        'COMPLETED': ' Terminé',
        'CANCELLED': ' Annulé'
      };
      return labels[status] || status;
    };

    const startConsultation = async (id) => {
      if (!confirm('Démarrer cette consultation ?')) return;
      try {
        await api.post(`/caregiver/appointments/${id}/status`, { status: 'COMPLETED' });
        const appt = appointments.value.find(a => a.id === id);
        if (appt) {
          appt.status = 'COMPLETED';
          alert(' Consultation démarrée !');
        }
      } catch (error) {
        console.error(' Erreur:', error);
        alert(' Erreur lors du démarrage');
      }
    };

    const openConsultationModal = (appt) => {
      selectedAppointment.value = appt;
      consultationReport.value = '';
      uploadedFiles.value = [];
      showModal.value = true;
    };

    const handleFileUpload = (event) => {
      uploadedFiles.value = Array.from(event.target.files);
    };

    const saveConsultation = async () => {
      if (!consultationReport.value.trim()) {
        alert('⚠️ Veuillez rédiger un compte-rendu');
        return;
      }

      saving.value = true;
      try {
        // 1. Créer la consultation
        const formData = new FormData();
        formData.append('appointment_id', selectedAppointment.value.id);
        formData.append('report', consultationReport.value);
        
        // Ajouter les fichiers
        uploadedFiles.value.forEach(file => {
          formData.append('files', file);
        });

        const response = await api.post('/caregiver/consultations', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        console.log(' Consultation créée:', response.data);
        alert('Compte-rendu enregistré avec succès !');
        
        // Marquer comme ayant une consultation
        const appt = appointments.value.find(a => a.id === selectedAppointment.value.id);
        if (appt) appt.has_consultation = true;
        
        showModal.value = false;
      } catch (error) {
        console.error(' Erreur:', error);
        alert(' Erreur lors de l\'enregistrement');
      } finally {
        saving.value = false;
      }
    };

    const viewConsultation = (id) => {
      // Rediriger vers le détail de la consultation
      router.push(`/app/doctor/consultations/${id}`);
    };

    const loadAppointments = async () => {
      loading.value = true;
      try {
        const response = await api.get('/caregiver/appointments');
        console.log(' Rendez-vous:', response.data);
        
        if (response.data && response.data.data) {
          appointments.value = response.data.data.map(appt => ({
            ...appt,
            has_consultation: false // À vérifier avec l'API
          }));
        }
      } catch (error) {
        console.error(' Erreur chargement:', error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadAppointments();
    });

    return {
      appointments,
      filteredConsultations,
      searchQuery,
      selectedFilter,
      loading,
      showModal,
      saving,
      selectedAppointment,
      consultationReport,
      formatDate,
      formatTime,
      getInitials,
      getStatusColor,
      getStatusBadge,
      getStatusLabel,
      startConsultation,
      openConsultationModal,
      handleFileUpload,
      saveConsultation,
      viewConsultation
    };
  }
};
</script>