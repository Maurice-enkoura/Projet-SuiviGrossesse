<!-- src/views/patient/DashboardView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Bonjour, {{ userName }}</h1>
      <p class="text-gray-500 text-sm">Voici un aperçu de votre suivi de grossesse</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement de votre tableau de bord...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Contenu -->
    <template v-else>
      <!-- Cartes de statistiques -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-rose-500 text-xs font-medium">Grossesses</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.pregnancies }}</p>
            </div>
            <div class="w-10 h-10 bg-rose-100 rounded-lg flex items-center justify-center">
              <Baby class="w-5 h-5 text-rose-500" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-500 text-xs font-medium">Rendez-vous</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.appointments }}</p>
            </div>
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Calendar class="w-5 h-5 text-green-500" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-500 text-xs font-medium">Examens</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.exams }}</p>
            </div>
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Activity class="w-5 h-5 text-purple-500" />
            </div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-amber-500 text-xs font-medium">Messages</p>
              <p class="text-2xl font-bold text-gray-800">{{ stats.messages }}</p>
            </div>
            <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
              <MessageCircle class="w-5 h-5 text-amber-500" />
            </div>
          </div>
        </div>
      </div>

      <!-- Grossesse active -->
      <div v-if="activePregnancy" class="bg-gradient-to-r from-rose-500 to-rose-600 rounded-xl p-6 text-white">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p class="text-rose-100 text-sm"> Grossesse active</p>
            <h2 class="text-2xl font-bold">Semaine {{ activePregnancy.week }}</h2>
            <p class="text-rose-100 text-sm mt-1">
              Débutée le {{ formatDate(activePregnancy.start_date) }} 
              • Accouchement prévu le {{ formatDate(activePregnancy.due_date) }}
            </p>
          </div>
          <div class="flex items-center gap-6">
            <div class="text-center">
              <p class="text-2xl font-bold">{{ activePregnancy.week }}</p>
              <p class="text-rose-100 text-xs">Semaines</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold">{{ activePregnancy.daysRemaining }}</p>
              <p class="text-rose-100 text-xs">Jours restants</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold">{{ activePregnancy.progress }}%</p>
              <p class="text-rose-100 text-xs">Progression</p>
            </div>
          </div>
        </div>
        <div class="mt-4 w-full bg-rose-400/30 rounded-full h-2">
          <div class="bg-white h-2 rounded-full transition-all duration-500" :style="{ width: activePregnancy.progress + '%' }"></div>
        </div>
      </div>

      <div v-else class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 text-center">
        <Baby class="w-16 h-16 text-rose-300 mx-auto mb-4" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucune grossesse active</h3>
        <p class="text-gray-500">Commencez à suivre votre grossesse dès maintenant</p>
        <router-link to="/app/patient/pregnancy/create" class="inline-flex items-center gap-2 mt-4 px-6 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition">
          <Plus class="w-4 h-4" /> Ajouter une grossesse
        </router-link>
      </div>

      <!-- Actions rapides -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <router-link to="/app/patient/pregnancy/create" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-rose-100">
          <div class="w-12 h-12 bg-rose-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <Plus class="w-6 h-6 text-rose-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Nouvelle grossesse</p>
        </router-link>
        <router-link to="/app/patient/appointment/create" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-rose-100">
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <CalendarPlus class="w-6 h-6 text-blue-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Prendre rendez-vous</p>
        </router-link>
        <router-link to="/app/patient/records" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-rose-100">
          <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FileText class="w-6 h-6 text-purple-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Mes dossiers</p>
        </router-link>
        <router-link to="/app/patient/messages" class="bg-white rounded-xl p-4 text-center hover:shadow-md transition border border-rose-100">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <MessageCircle class="w-6 h-6 text-green-500" />
          </div>
          <p class="text-sm font-medium text-gray-700">Messages</p>
        </router-link>
      </div>

      <!-- Prochains rendez-vous -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">📅 Prochains rendez-vous</h3>
          <router-link to="/app/patient/appointments" class="text-rose-500 text-sm hover:underline">Voir tout</router-link>
        </div>
        <div v-if="upcomingAppointments.length > 0" class="space-y-3">
          <div v-for="appt in upcomingAppointments" :key="appt.id" class="flex items-center justify-between p-3 bg-rose-50 rounded-lg">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-rose-100 rounded-full flex items-center justify-center text-rose-600">
                <User class="w-5 h-5" />
              </div>
              <div>
                <p class="font-medium text-gray-800">{{ appt.caregiver_name || 'Médecin' }}</p>
                <p class="text-sm text-gray-500">{{ formatDate(appt.date_time) }} à {{ formatTime(appt.date_time) }}</p>
                <p class="text-xs text-gray-400">{{ appt.reason || 'Consultation' }}</p>
              </div>
            </div>
            <span class="px-2 py-1 rounded-full text-xs font-medium" :class="appt.status === 'CONFIRMED' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'">
              {{ appt.status === 'CONFIRMED' ? ' Confirmé' : ' En attente' }}
            </span>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <Calendar class="w-12 h-12 text-gray-300 mx-auto mb-2" />
          <p class="text-gray-500">Aucun rendez-vous à venir</p>
          <router-link to="/app/patient/appointment/create" class="text-rose-500 text-sm hover:underline">Prendre rendez-vous</router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { 
  Baby, Calendar, Activity, MessageCircle, Plus, CalendarPlus, 
  FileText, User, Loader2
} from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'PatientDashboardView',
  components: {
    Baby, Calendar, Activity, MessageCircle, Plus, CalendarPlus,
    FileText, User, Loader2
  },
  setup() {
    const authStore = useAuthStore();
    const loading = ref(true);
    const error = ref('');

    const user = computed(() => authStore.user);
    const userName = computed(() => {
      return user.value?.username || user.value?.name || 'Patiente';
    });

    const stats = ref({
      pregnancies: 0,
      appointments: 0,
      exams: 0,
      messages: 0
    });

    const activePregnancy = ref(null);
    const upcomingAppointments = ref([]);

    const formatTime = (dateTime) => {
      if (!dateTime) return '';
      try {
        const d = new Date(dateTime);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '';
      }
    };

    const calculateWeek = (startDate) => {
      if (!startDate) return 0;
      const start = new Date(startDate);
      const now = new Date();
      const diff = Math.floor((now - start) / (1000 * 60 * 60 * 24 * 7));
      return Math.min(diff + 1, 42);
    };

    const calculateDaysRemaining = (dueDate) => {
      if (!dueDate) return 0;
      const due = new Date(dueDate);
      const now = new Date();
      const diff = Math.ceil((due - now) / (1000 * 60 * 60 * 24));
      return Math.max(diff, 0);
    };

    const loadDashboard = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log('📤 Chargement dashboard patient...');

        // 1. Récupérer les grossesses
        const pregnanciesRes = await api.get('/patient/pregnancies');
        console.log('📥 Grossesses:', pregnanciesRes.data);
        
        let pregnancies = [];
        if (pregnanciesRes.data && pregnanciesRes.data.data) {
          pregnancies = pregnanciesRes.data.data;
        }
        
        // Compter les grossesses
        stats.value.pregnancies = pregnancies.length;
        
        // Trouver la grossesse active
        const active = pregnancies.find(p => p.is_active === true);
        if (active) {
          const week = calculateWeek(active.start_date);
          const daysRemaining = calculateDaysRemaining(active.expected_delivery_date);
          activePregnancy.value = {
            id: active.id,
            start_date: active.start_date,
            due_date: active.expected_delivery_date,
            week: week,
            daysRemaining: daysRemaining,
            progress: Math.min((week / 40) * 100, 100)
          };
        }

        // 2. Récupérer les rendez-vous
        const appointmentsRes = await api.get('/patient/appointments');
        console.log(' Rendez-vous:', appointmentsRes.data);
        
        let appointments = [];
        if (appointmentsRes.data && appointmentsRes.data.data) {
          appointments = appointmentsRes.data.data;
        }
        
        stats.value.appointments = appointments.length;
        
        // Filtrer les rendez-vous à venir (SCHEDULED ou CONFIRMED)
        upcomingAppointments.value = appointments
          .filter(a => a.status === 'SCHEDULED' || a.status === 'CONFIRMED')
          .sort((a, b) => new Date(a.date_time) - new Date(b.date_time))
          .slice(0, 5);

        // 3. Récupérer les examens
        const examsRes = await api.get('/patient/exams');
        console.log('📥 Examens:', examsRes.data);
        
        if (examsRes.data && examsRes.data.data) {
          stats.value.exams = examsRes.data.data.length;
        }

        // 4. Récupérer les messages (si disponible)
        try {
          const messagesRes = await api.get('/patient/messages');
          if (messagesRes.data && messagesRes.data.data) {
            stats.value.messages = messagesRes.data.data.length;
          }
        } catch (e) {
          console.log('Messagerie non disponible');
          stats.value.messages = 0;
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
      user,
      userName,
      stats,
      activePregnancy,
      upcomingAppointments,
      loading,
      error,
      formatDate,
      formatTime
    };
  }
};
</script>