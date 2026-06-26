<!-- src/views/patient/PregnancyView.vue -->
<template>
  <div class="space-y-6">
    <div class="flex items-center gap-3">
      <button @click="$router.back()" class="p-2 rounded-lg hover:bg-rose-50 transition">
        <ArrowLeft class="w-5 h-5 text-gray-600" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Suivi de grossesse</h1>
        <p class="text-gray-500 text-sm">Semaine {{ currentWeek }} • Débutée le {{ formatDate(pregnancy?.start_date) }}</p>
      </div>
      <div class="ml-auto flex gap-2">
        <router-link to="/app/patient/appointment/create" class="bg-rose-500 text-white px-4 py-2 rounded-lg hover:bg-rose-600 transition text-sm flex items-center gap-2">
          <CalendarPlus class="w-4 h-4" /> Rendez-vous
        </router-link>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <div v-if="!loading && pregnancy" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Colonne gauche -->
      <div class="lg:col-span-1 space-y-4">
        <div class="bg-white rounded-xl p-5 shadow-sm border border-rose-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Informations</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between"><span class="text-gray-500">Semaine</span><span class="font-bold text-rose-600">{{ currentWeek }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Date de début</span><span>{{ formatDate(pregnancy.start_date) }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Date prévue</span><span>{{ formatDate(pregnancy.expected_delivery_date) }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Jours restants</span><span class="font-bold text-rose-600">{{ daysRemaining }}</span></div>
            <div class="flex justify-between"><span class="text-gray-500">Statut</span><span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="pregnancy.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'">{{ pregnancy.is_active ? '✅ Active' : '❌ Terminée' }}</span></div>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 shadow-sm border border-rose-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Progression</h3>
          <div class="relative pt-2">
            <div class="flex justify-between text-xs text-gray-500 mb-1">
              <span>Début</span><span>{{ currentWeek }} sem</span><span>Accouchement</span>
            </div>
            <div class="w-full bg-rose-100 rounded-full h-3">
              <div class="bg-gradient-to-r from-rose-400 to-rose-600 h-3 rounded-full transition-all duration-500" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <div class="text-center mt-2 text-sm text-gray-600">{{ progressPercentage }}% complété</div>
          </div>
        </div>

        <div class="bg-white rounded-xl p-5 shadow-sm border border-rose-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Conseils</h3>
          <div class="bg-rose-50 rounded-lg p-4">
            <p class="text-sm text-rose-800">{{ currentAdvice }}</p>
          </div>
        </div>
      </div>

      <!-- Colonne droite -->
      <div class="lg:col-span-2 space-y-4">
        <!-- Rendez-vous -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-rose-100">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-semibold text-gray-800"> Rendez-vous</h3>
            <router-link to="/app/patient/appointment/create" class="text-rose-500 text-sm hover:underline">+ Ajouter</router-link>
          </div>
          <div v-if="appointments.length > 0" class="space-y-2">
            <div v-for="appt in appointments" :key="appt.id" class="flex items-center justify-between p-3 bg-rose-50 rounded-lg">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-rose-100 rounded-full flex items-center justify-center">
                  <User class="w-5 h-5 text-rose-500" />
                </div>
                <div>
                  <p class="font-medium text-gray-800">{{ appt.caregiver_name || 'Médecin' }}</p>
                  <p class="text-sm text-gray-500">{{ formatDate(appt.date_time) }} à {{ formatTime(appt.date_time) }}</p>
                  <p class="text-xs text-gray-400">{{ appt.reason || 'Consultation' }}</p>
                </div>
              </div>
              <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getStatusClass(appt.status)">
                {{ getStatusLabel(appt.status) }}
              </span>
            </div>
          </div>
          <div v-else class="text-center py-6">
            <Calendar class="w-12 h-12 text-gray-300 mx-auto mb-2" />
            <p class="text-gray-500">Aucun rendez-vous</p>
          </div>
        </div>

        <!-- Examens médicaux -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-rose-100">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-semibold text-gray-800"> Examens médicaux</h3>
          </div>
          <div v-if="exams.length > 0" class="space-y-2">
            <div 
              v-for="exam in exams" 
              :key="exam.id" 
              class="flex items-center justify-between p-3 bg-rose-50 rounded-lg hover:bg-rose-100 transition cursor-pointer"
              @click="viewExam(exam.id)"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                  <Activity class="w-5 h-5 text-purple-500" />
                </div>
                <div>
                  <p class="font-medium text-gray-800">{{ exam.exam_type_display || exam.exam_type }}</p>
                  <p class="text-sm text-gray-500">{{ formatDate(exam.exam_date) }}</p>
                  <p class="text-xs text-gray-400">{{ exam.result_summary || 'En attente des résultats' }}</p>
                  <!-- Indicateur de fichiers joints -->
                  <span v-if="exam.file_attachment" class="text-xs text-blue-500 flex items-center gap-1 mt-1">
                    <FileText class="w-3 h-3" /> Fichier joint
                  </span>
                </div>
              </div>
              <div class="flex flex-col items-end gap-1">
                <span class="px-2 py-1 rounded-full text-xs font-medium" :class="exam.is_abnormal ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'">
                  {{ exam.is_abnormal ? ' Anormal' : ' Normal' }}
                </span>
                <button 
                  @click.stop="viewExam(exam.id)" 
                  class="text-xs text-purple-500 hover:underline"
                >
                  Voir détails →
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-6">
            <Activity class="w-12 h-12 text-gray-300 mx-auto mb-2" />
            <p class="text-gray-500">Aucun examen</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Chargement -->
    <div v-else-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement...</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeft, CalendarPlus, Calendar, User, Activity, Loader2, FileText } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'PregnancyView',
  components: { ArrowLeft, CalendarPlus, Calendar, User, Activity, Loader2, FileText },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const pregnancy = ref(null);
    const appointments = ref([]);
    const exams = ref([]);
    const loading = ref(true);
    const error = ref('');

    const currentWeek = computed(() => {
      if (!pregnancy.value?.start_date) return 0;
      const start = new Date(pregnancy.value.start_date);
      const now = new Date();
      const diff = Math.floor((now - start) / (1000 * 60 * 60 * 24 * 7));
      return Math.min(diff + 1, 42);
    });

    const daysRemaining = computed(() => {
      if (!pregnancy.value?.expected_delivery_date) return 0;
      const due = new Date(pregnancy.value.expected_delivery_date);
      const now = new Date();
      const diff = Math.ceil((due - now) / (1000 * 60 * 60 * 24));
      return Math.max(diff, 0);
    });

    const progressPercentage = computed(() => Math.min((currentWeek.value / 40) * 100, 100));

    const currentAdvice = computed(() => {
      const week = currentWeek.value;
      if (week <= 12) return 'Profitez de cette période pour bien vous reposer et prendre soin de vous.';
      if (week <= 20) return 'Vous pouvez commencer à sentir les mouvements du bébé.';
      if (week <= 30) return 'Le bébé grandit rapidement. Pensez à préparer la chambre.';
      if (week <= 40) return 'La grande date approche ! Restez calme.';
      return 'Félicitations ! Profitez de chaque instant.';
    });

    const formatTime = (dateTime) => {
      if (!dateTime) return '';
      try {
        const d = new Date(dateTime);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '';
      }
    };

    const getStatusClass = (status) => {
      const classes = {
        'SCHEDULED': 'bg-blue-100 text-blue-700',
        'CONFIRMED': 'bg-green-100 text-green-700',
        'COMPLETED': 'bg-purple-100 text-purple-700',
        'CANCELLED': 'bg-red-100 text-red-700'
      };
      return classes[status] || 'bg-gray-100 text-gray-700';
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

    const viewExam = (examId) => {
      router.push(`/app/patient/records/${examId}`);
    };

    const loadData = async () => {
      const id = route.params.id;
      if (!id) {
        error.value = 'ID de grossesse manquant';
        loading.value = false;
        return;
      }
      
      loading.value = true;
      error.value = '';
      
      try {
        console.log(' Chargement grossesse ID:', id);
        
        // 1. Charger la grossesse
        const pregnancyResponse = await api.get(`/patient/pregnancies/${id}`);
        console.log(' Grossesse:', pregnancyResponse.data);
        
        if (pregnancyResponse.data && pregnancyResponse.data.data) {
          pregnancy.value = pregnancyResponse.data.data;
        } else {
          pregnancy.value = pregnancyResponse.data;
        }

        // 2. Charger tous les rendez-vous de la patiente
        const appointmentsResponse = await api.get('/patient/appointments');
        console.log(' Rendez-vous:', appointmentsResponse.data);
        
        if (appointmentsResponse.data && appointmentsResponse.data.data) {
          appointments.value = appointmentsResponse.data.data.filter(
            appt => appt.pregnancy === parseInt(id)
          );
        }

        // 3. Charger tous les examens de la patiente
        const examsResponse = await api.get('/patient/exams');
        console.log(' Examens:', examsResponse.data);
        
        if (examsResponse.data && examsResponse.data.data) {
          exams.value = examsResponse.data.data;
        }
        
      } catch (error) {
        console.error(' Erreur chargement données:', error);
        error.value = error.response?.data?.message || 'Erreur lors du chargement des données';
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadData();
    });

    return {
      pregnancy,
      appointments,
      exams,
      loading,
      error,
      currentWeek,
      daysRemaining,
      progressPercentage,
      currentAdvice,
      formatDate,
      formatTime,
      getStatusClass,
      getStatusLabel,
      viewExam
    };
  }
};
</script>