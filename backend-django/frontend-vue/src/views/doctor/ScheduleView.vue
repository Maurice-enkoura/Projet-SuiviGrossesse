<!-- src/views/doctor/ScheduleView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Mes horaires de consultation</h1>
      <p class="text-gray-500 text-sm">Définissez vos jours et heures de consultation</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des horaires...</p>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Formulaire -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="day in daysOfWeek" :key="day.value" class="bg-white rounded-xl p-5 shadow-sm border border-blue-100">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-semibold text-gray-800">{{ day.label }}</h3>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="day.is_working" class="sr-only peer" />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
          </label>
        </div>

        <div v-if="day.is_working" class="space-y-3">
          <div>
            <label class="text-sm text-gray-600">Matin</label>
            <div class="flex gap-2 mt-1">
              <input type="time" v-model="day.morning_start" class="flex-1 px-3 py-1 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-400" />
              <span class="text-gray-400 self-center">à</span>
              <input type="time" v-model="day.morning_end" class="flex-1 px-3 py-1 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-400" />
            </div>
          </div>
          <div>
            <label class="text-sm text-gray-600">Après-midi</label>
            <div class="flex gap-2 mt-1">
              <input type="time" v-model="day.afternoon_start" class="flex-1 px-3 py-1 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-400" />
              <span class="text-gray-400 self-center">à</span>
              <input type="time" v-model="day.afternoon_end" class="flex-1 px-3 py-1 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-400" />
            </div>
          </div>
          <div>
            <label class="text-sm text-gray-600">Durée des créneaux</label>
            <select v-model="day.slot_duration" class="w-full mt-1 px-3 py-1 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-blue-400">
              <option value="15">15 min</option>
              <option value="20">20 min</option>
              <option value="30" selected>30 min</option>
              <option value="45">45 min</option>
              <option value="60">60 min</option>
            </select>
          </div>
        </div>

        <div v-else class="text-center py-4 text-gray-400 text-sm">
          Jour non travaillé
        </div>
      </div>
    </div>

    <!-- Aperçu des créneaux -->
    <div class="bg-white rounded-xl p-5 shadow-sm border border-blue-100">
      <h3 class="font-semibold text-gray-800 mb-3"> Aperçu des créneaux générés</h3>
      <div v-if="hasSchedule" class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div v-for="day in activeDays" :key="day.value" class="p-3 bg-blue-50 rounded-lg">
          <p class="font-medium text-gray-800 text-sm">{{ day.label }}</p>
          <p class="text-xs text-gray-500 mt-1">
            Matin: {{ day.morning_start || '-' }} - {{ day.morning_end || '-' }}
          </p>
          <p class="text-xs text-gray-500">
            Après-midi: {{ day.afternoon_start || '-' }} - {{ day.afternoon_end || '-' }}
          </p>
          <p class="text-xs text-blue-600 mt-1">
            Créneaux de {{ day.slot_duration }} min
          </p>
        </div>
      </div>
      <div v-else class="text-center py-6 text-gray-500">
        Aucun jour de consultation défini
      </div>
    </div>

    <!-- Boutons -->
    <div class="flex gap-3">
      <button @click="saveSchedule" class="bg-blue-500 text-white px-6 py-2.5 rounded-lg hover:bg-blue-600 transition font-medium flex items-center gap-2 disabled:opacity-50" :disabled="saving">
        <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
        {{ saving ? 'Enregistrement...' : '💾 Enregistrer les horaires' }}
      </button>
      <button @click="resetSchedule" class="px-6 py-2.5 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
        Réinitialiser
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Loader2 } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'DoctorScheduleView',
  components: { Loader2 },
  setup() {
    const saving = ref(false);
    const loading = ref(true);
    const error = ref('');

    const daysOfWeek = ref([
      { value: 0, label: 'Lundi', is_working: true, morning_start: '09:00', morning_end: '12:00', afternoon_start: '14:00', afternoon_end: '17:00', slot_duration: 30 },
      { value: 1, label: 'Mardi', is_working: true, morning_start: '09:00', morning_end: '12:00', afternoon_start: '14:00', afternoon_end: '17:00', slot_duration: 30 },
      { value: 2, label: 'Mercredi', is_working: true, morning_start: '09:00', morning_end: '12:00', afternoon_start: '14:00', afternoon_end: '17:00', slot_duration: 30 },
      { value: 3, label: 'Jeudi', is_working: true, morning_start: '09:00', morning_end: '12:00', afternoon_start: '14:00', afternoon_end: '17:00', slot_duration: 30 },
      { value: 4, label: 'Vendredi', is_working: true, morning_start: '09:00', morning_end: '12:00', afternoon_start: '14:00', afternoon_end: '17:00', slot_duration: 30 },
      { value: 5, label: 'Samedi', is_working: false, morning_start: '09:00', morning_end: '12:00', afternoon_start: '', afternoon_end: '', slot_duration: 30 },
      { value: 6, label: 'Dimanche', is_working: false, morning_start: '', morning_end: '', afternoon_start: '', afternoon_end: '', slot_duration: 30 }
    ]);

    const hasSchedule = computed(() => {
      return daysOfWeek.value.some(d => d.is_working);
    });

    const activeDays = computed(() => {
      return daysOfWeek.value.filter(d => d.is_working);
    });

    const loadSchedule = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await api.get('/caregiver/schedule');
        console.log('📥 Horaires:', response.data);
        
        if (response.data && response.data.data && response.data.data.length > 0) {
          const schedules = response.data.data;
          
          // Mettre à jour les jours avec les données de l'API
          daysOfWeek.value.forEach(day => {
            const found = schedules.find(s => s.day_of_week === day.value);
            if (found) {
              day.is_working = found.is_working;
              day.morning_start = found.morning_start || '';
              day.morning_end = found.morning_end || '';
              day.afternoon_start = found.afternoon_start || '';
              day.afternoon_end = found.afternoon_end || '';
              day.slot_duration = found.slot_duration || 30;
            }
          });
        }
      } catch (err) {
        console.error(' Erreur chargement horaires:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement des horaires';
      } finally {
        loading.value = false;
      }
    };

    const saveSchedule = async () => {
      saving.value = true;
      error.value = '';
      
      try {
        const schedules = daysOfWeek.value.map(day => ({
          day_of_week: day.value,
          is_working: day.is_working,
          morning_start: day.morning_start || null,
          morning_end: day.morning_end || null,
          afternoon_start: day.afternoon_start || null,
          afternoon_end: day.afternoon_end || null,
          slot_duration: day.slot_duration
        }));
        
        console.log(' Sauvegarde des horaires:', schedules);
        
        const response = await api.post('/caregiver/schedule', { schedules });
        console.log(' Réponse:', response.data);
        
        alert(' Horaires enregistrés avec succès !');
      } catch (err) {
        console.error(' Erreur sauvegarde:', err);
        error.value = err.response?.data?.message || 'Erreur lors de la sauvegarde';
        alert(' Erreur lors de la sauvegarde des horaires');
      } finally {
        saving.value = false;
      }
    };

    const resetSchedule = () => {
      if (!confirm('Réinitialiser tous les horaires ?')) return;
      
      daysOfWeek.value.forEach(day => {
        if (day.value <= 4) { // Lundi à Vendredi
          day.is_working = true;
          day.morning_start = '09:00';
          day.morning_end = '12:00';
          day.afternoon_start = '14:00';
          day.afternoon_end = '17:00';
          day.slot_duration = 30;
        } else { // Samedi et Dimanche
          day.is_working = false;
          day.morning_start = '';
          day.morning_end = '';
          day.afternoon_start = '';
          day.afternoon_end = '';
          day.slot_duration = 30;
        }
      });
    };

    onMounted(() => {
      loadSchedule();
    });

    return {
      daysOfWeek,
      activeDays,
      hasSchedule,
      loading,
      saving,
      error,
      saveSchedule,
      resetSchedule
    };
  }
};
</script>