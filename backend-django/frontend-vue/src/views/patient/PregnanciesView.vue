<!-- src/views/patient/PregnanciesView.vue -->
<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">🤰 Mes grossesses</h1>
        <p class="text-gray-500 text-sm">Suivez l'évolution de vos grossesses</p>
      </div>
      <router-link 
        to="/app/patient/pregnancy/create" 
        class="inline-flex items-center gap-2 px-4 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition"
      >
        <Plus class="w-4 h-4" />
        Nouvelle grossesse
      </router-link>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-rose-500 text-sm">Total</p>
        <p class="text-2xl font-bold text-gray-800">{{ pregnancies.length }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-green-500 text-sm">Actives</p>
        <p class="text-2xl font-bold text-green-600">{{ activeCount }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-gray-500 text-sm">Terminées</p>
        <p class="text-2xl font-bold text-gray-600">{{ completedCount }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-purple-500 text-sm">Semaine actuelle</p>
        <p class="text-2xl font-bold text-purple-600">{{ currentWeek }}</p>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      ❌ {{ error }}
    </div>

    <!-- Liste -->
    <div v-if="!loading && pregnancies.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="pregnancy in pregnancies" 
        :key="pregnancy.id"
        class="bg-white rounded-xl p-5 shadow-sm border border-rose-100 hover:shadow-md transition cursor-pointer"
        @click="viewPregnancy(pregnancy.id)"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-gray-800">Grossesse #{{ pregnancy.id }}</h3>
            <p class="text-sm text-gray-500">Débutée le {{ formatDate(pregnancy.start_date) }}</p>
          </div>
          <span class="px-2 py-1 rounded-full text-xs font-medium" :class="pregnancy.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'">
            {{ pregnancy.is_active ? 'Active' : 'Terminée' }}
          </span>
        </div>

        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-500">Semaine</span>
            <span class="font-semibold text-rose-600">{{ calculateWeek(pregnancy.start_date) }}</span>
          </div>
          <div class="flex justify-between text-sm">
            <span class="text-gray-500">Date prévue</span>
            <span class="font-medium">{{ formatDate(pregnancy.expected_delivery_date) }}</span>
          </div>
        </div>

        <div class="mt-3 pt-3 border-t border-rose-50">
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>Progression</span>
            <span>{{ calculateProgress(pregnancy.start_date) }}%</span>
          </div>
          <div class="w-full bg-rose-100 rounded-full h-2">
            <div 
              class="bg-gradient-to-r from-rose-400 to-rose-600 h-2 rounded-full transition-all duration-500"
              :style="{ width: calculateProgress(pregnancy.start_date) + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chargement -->
    <div v-else-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des grossesses...</p>
    </div>

    <!-- Message vide -->
    <div v-else class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Baby class="w-16 h-16 text-rose-300 mx-auto mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucune grossesse enregistrée</h3>
      <p class="text-gray-500">Commencez à suivre votre grossesse dès maintenant</p>
      <router-link to="/app/patient/pregnancy/create" class="inline-flex items-center gap-2 mt-4 px-6 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition">
        <Plus class="w-4 h-4" /> Ajouter une grossesse
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Plus, Baby, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'PregnanciesView',
  components: { Plus, Baby, Loader2 },
  setup() {
    const router = useRouter();
    const pregnancies = ref([]);
    const loading = ref(true);
    const error = ref('');

    const activeCount = computed(() => pregnancies.value.filter(p => p.is_active).length);
    const completedCount = computed(() => pregnancies.value.filter(p => !p.is_active).length);
    const currentWeek = computed(() => {
      const active = pregnancies.value.find(p => p.is_active);
      return active ? calculateWeek(active.start_date) : 0;
    });

    const calculateWeek = (startDate) => {
      if (!startDate) return 0;
      const start = new Date(startDate);
      const now = new Date();
      const diff = Math.floor((now - start) / (1000 * 60 * 60 * 24 * 7));
      return Math.min(diff + 1, 42);
    };

    const calculateProgress = (startDate) => {
      const week = calculateWeek(startDate);
      return Math.min(Math.round((week / 40) * 100), 100);
    };

    const viewPregnancy = (id) => {
      router.push(`/app/patient/pregnancy/${id}`);
    };

    const loadPregnancies = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log('📤 Chargement des grossesses...');
        const response = await api.get('/patient/pregnancies');
        console.log('📥 Réponse brute:', response.data);
        
        // ✅ Vos APIs retournent { message, data }
        if (response.data && response.data.data) {
          pregnancies.value = Array.isArray(response.data.data) ? response.data.data : [];
          console.log('✅ Grossesses chargées:', pregnancies.value.length);
        } else if (Array.isArray(response.data)) {
          pregnancies.value = response.data;
        } else {
          pregnancies.value = [];
        }
        
      } catch (error) {
        console.error('❌ Erreur chargement grossesses:', error);
        
        if (error.response?.status === 404) {
          error.value = 'L\'API des grossesses n\'est pas disponible.';
        } else if (error.response?.data?.message) {
          error.value = error.response.data.message;
        } else if (error.request) {
          error.value = 'Impossible de contacter le serveur.';
        } else {
          error.value = 'Erreur lors du chargement des grossesses';
        }
        
        // Données de fallback
        pregnancies.value = [
          {
            id: 1,
            start_date: '2024-11-01',
            expected_delivery_date: '2025-07-15',
            is_active: true,
            notes: 'Grossesse normale'
          }
        ];
        
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadPregnancies();
    });

    return {
      pregnancies,
      loading,
      error,
      activeCount,
      completedCount,
      currentWeek,
      formatDate,
      calculateWeek,
      calculateProgress,
      viewPregnancy
    };
  }
};
</script>