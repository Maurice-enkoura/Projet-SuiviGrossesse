<!-- src/views/doctor/DashboardView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800">📊 Tableau de bord</h1>
      <p class="text-gray-500 text-sm">Bonjour, Dr. {{ doctorName }}</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des données...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      ❌ {{ error }}
    </div>

    <!-- Contenu -->
    <template v-else>
      <!-- Cartes de statistiques -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-sm border border-blue-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-500 text-xs font-medium">Patientes</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.patients }}</p>
            </div>
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Users class="w-5 h-5 text-blue-500" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-green-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-500 text-xs font-medium">Rendez-vous aujourd'hui</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.todayAppointments }}</p>
            </div>
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Calendar class="w-5 h-5 text-green-500" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-purple-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-500 text-xs font-medium">Grossesses suivies</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.pregnancies }}</p>
            </div>
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Baby class="w-5 h-5 text-purple-500" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-amber-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-amber-500 text-xs font-medium">En attente</p>
              <p class="text-2xl font-bold text-amber-500">{{ stats.pending }}</p>
            </div>
            <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
              <Clock class="w-5 h-5 text-amber-500" />
            </div>
          </div>
        </div>
      </div>

      <!-- Actions rapides -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <router-link to="/app/doctor/patients" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-blue-100">
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <Users class="w-6 h-6 text-blue-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Mes patientes</p>
        </router-link>
        <router-link to="/app/doctor/appointments" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-green-100">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <Calendar class="w-6 h-6 text-green-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Rendez-vous</p>
        </router-link>
        <router-link to="/app/doctor/schedule" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-purple-100">
          <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <Clock class="w-6 h-6 text-purple-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Mes horaires</p>
        </router-link>
        <router-link to="/app/doctor/consultations" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-amber-100">
          <div class="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <Stethoscope class="w-6 h-6 text-amber-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Consultations</p>
        </router-link>
      </div>

      <!-- Rendez-vous du jour -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-blue-100">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">📅 Rendez-vous du jour</h3>
          <router-link to="/app/doctor/appointments" class="text-blue-500 text-sm hover:underline">Voir tout</router-link>
        </div>
        
        <div v-if="todayAppointments.length > 0" class="space-y-3">
          <div v-for="appt in todayAppointments" :key="appt.id" class="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                {{ getInitials(appt.patient_name) }}
              </div>
              <div>
                <p class="font-medium text-gray-800">{{ appt.patient_name || 'Patiente' }}</p>
                <p class="text-sm text-gray-500">{{ appt.reason || 'Consultation' }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-sm text-gray-600">{{ formatTime(appt.date_time) }}</span>
              <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getStatusClass(appt.status)">
                {{ getStatusLabel(appt.status) }}
              </span>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8">
          <Calendar class="w-12 h-12 text-gray-300 mx-auto mb-2" />
          <p class="text-gray-500">Aucun rendez-vous aujourd'hui</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { Users, Calendar, Baby, Clock, Stethoscope, Loader2 } from 'lucide-vue-next';
import api from '@/services/api';
import { formatDate, getInitials } from '@/utils/helpers';

export default {
  name: 'DoctorDashboardView',
  components: { Users, Calendar, Baby, Clock, Stethoscope, Loader2 },
  setup() {
    const authStore = useAuthStore();
    const user = computed(() => authStore.user);
    const loading = ref(true);
    const error = ref('');
    
    const doctorName = computed(() => {
      return user.value?.username || user.value?.name || 'Médecin';
    });

    const stats = ref({
      patients: 0,
      todayAppointments: 0,
      pregnancies: 0,
      pending: 0
    });
    
    const todayAppointments = ref([]);

    const formatTime = (dateTime) => {
      if (!dateTime) return '-';
      try {
        const d = new Date(dateTime);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '-';
      }
    };

    const getStatusClass = (status) => {
      const classes = {
        'SCHEDULED': 'bg-yellow-100 text-yellow-700',
        'CONFIRMED': 'bg-green-100 text-green-700',
        'COMPLETED': 'bg-purple-100 text-purple-700',
        'CANCELLED': 'bg-red-100 text-red-700'
      };
      return classes[status] || 'bg-gray-100 text-gray-700';
    };

    const getStatusLabel = (status) => {
      const labels = {
        'SCHEDULED': '⏳ En attente',
        'CONFIRMED': '✅ Confirmé',
        'COMPLETED': '✔️ Terminé',
        'CANCELLED': '❌ Annulé'
      };
      return labels[status] || status;
    };

    const loadDashboard = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log('📤 Chargement dashboard médecin...');
        console.log('👤 Utilisateur connecté:', user.value);

        // 1. Récupérer les patientes du médecin
        const patientsRes = await api.get('/caregiver/patients');
        console.log('📥 Réponse patientes brute:', patientsRes.data);
        
        let patients = [];
        if (patientsRes.data && patientsRes.data.data) {
          patients = patientsRes.data.data;
          console.log('✅ Patientes trouvées:', patients.length);
        } else if (Array.isArray(patientsRes.data)) {
          patients = patientsRes.data;
        } else {
          console.warn('⚠️ Aucune patiente trouvée');
        }
        stats.value.patients = patients.length;

        // 2. Récupérer les rendez-vous du médecin
        const appointmentsRes = await api.get('/caregiver/appointments');
        console.log('📥 Réponse rendez-vous brute:', appointmentsRes.data);
        
        let appointments = [];
        if (appointmentsRes.data && appointmentsRes.data.data) {
          appointments = appointmentsRes.data.data;
          console.log('✅ Rendez-vous trouvés:', appointments.length);
        } else if (Array.isArray(appointmentsRes.data)) {
          appointments = appointmentsRes.data;
        }
        
        // Rendez-vous du jour
        const today = new Date().toISOString().split('T')[0];
        console.log('📅 Date du jour:', today);
        
        todayAppointments.value = appointments.filter(a => {
          if (!a.date_time) return false;
          return a.date_time.startsWith(today);
        });
        stats.value.todayAppointments = todayAppointments.value.length;
        console.log('✅ Rendez-vous aujourd\'hui:', stats.value.todayAppointments);
        
        // En attente (SCHEDULED)
        stats.value.pending = appointments.filter(a => 
          a.status === 'SCHEDULED'
        ).length;
        console.log('✅ Rendez-vous en attente:', stats.value.pending);

        // 3. Compter les grossesses actives des patientes
        let pregnanciesCount = 0;
        for (const patient of patients) {
          try {
            // Récupérer les grossesses de la patiente
            const pregRes = await api.get(`/patient/pregnancies`);
            console.log(`📥 Grossesses pour patient ${patient.id}:`, pregRes.data);
            
            if (pregRes.data && pregRes.data.data) {
              // Compter les grossesses actives de cette patiente
              const activePregnancies = pregRes.data.data.filter(
                p => p.patient === patient.id && p.is_active === true
              );
              pregnanciesCount += activePregnancies.length;
            }
          } catch (e) {
            console.log(`ℹ️ Pas de grossesse pour patient ${patient.id}`);
          }
        }
        stats.value.pregnancies = pregnanciesCount;
        console.log('✅ Total grossesses suivies:', stats.value.pregnancies);

        console.log('📊 Statistiques finales:', stats.value);

      } catch (error) {
        console.error('❌ Erreur chargement dashboard:', error);
        error.value = error.response?.data?.message || error.message || 'Erreur lors du chargement';
        
        // Données de fallback
        stats.value = {
          patients: 0,
          todayAppointments: 0,
          pregnancies: 0,
          pending: 0
        };
        todayAppointments.value = [];
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadDashboard();
    });

    return { 
      user, 
      doctorName,
      stats, 
      todayAppointments,
      loading,
      error,
      formatDate,
      formatTime,
      getInitials,
      getStatusClass,
      getStatusLabel
    };
  }
};
</script>