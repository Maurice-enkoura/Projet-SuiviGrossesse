<!-- src/views/patient/AppointmentCreateView.vue -->
<template>
  <div class="max-w-2xl mx-auto">
    <div class="flex items-center gap-3 mb-6">
      <button @click="$router.back()" class="p-2 rounded-lg hover:bg-rose-50 transition">
        <ArrowLeft class="w-5 h-5 text-gray-600" />
      </button>
      <h1 class="text-2xl font-bold text-gray-800"> Prendre rendez-vous</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 space-y-5">
      <!-- Messages -->
      <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
         {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
         {{ successMessage }}
      </div>

      <!-- Grossesse active (automatique) -->
      <div class="bg-rose-50 rounded-lg p-4 border border-rose-200">
        <div class="flex items-center gap-3">
          <Baby class="w-5 h-5 text-rose-500" />
          <div>
            <p class="text-sm text-gray-600">Grossesse suivie</p>
            <p v-if="activePregnancy" class="font-medium text-gray-800">
              Grossesse #{{ activePregnancy.id }} - {{ formatDate(activePregnancy.start_date) }}
              <span class="text-xs text-gray-500 ml-2">(Semaine {{ activePregnancyWeek }})</span>
            </p>
            <p v-else class="text-amber-600 text-sm">
               Aucune grossesse active. Créez d'abord une grossesse.
            </p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- 1. Choix du médecin -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Médecin *</label>
          <select 
            v-model="form.caregiver_id" 
            @change="generateSlots"
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" 
            required
          >
            <option value="">Sélectionner un médecin</option>
            <option v-for="doctor in doctors" :key="doctor.id" :value="doctor.id">
              {{ doctor.name }} - {{ doctor.speciality }}
            </option>
          </select>
        </div>

        <!-- 2. Choix de la date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date *</label>
          <input 
            v-model="form.date" 
            type="date" 
            @change="generateSlots"
            :min="minDate"
            :max="maxDate"
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" 
            required 
          />
          <p class="text-xs text-gray-400 mt-1">Du {{ formatDate(minDate) }} au {{ formatDate(maxDate) }}</p>
        </div>

        <!-- 3. Créneaux disponibles -->
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Créneau disponible *</label>
          
          <!-- Grille des créneaux -->
          <div v-if="availableSlots.length > 0" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
            <button
              v-for="slot in availableSlots"
              :key="slot"
              type="button"
              @click="selectSlot(slot)"
              class="py-2 px-3 rounded-lg text-sm font-medium transition border"
              :class="form.time_slot === slot 
                ? 'bg-rose-500 text-white border-rose-500' 
                : 'bg-white text-gray-700 border-gray-200 hover:border-rose-300 hover:bg-rose-50'"
            >
              {{ slot }}
            </button>
          </div>
          
          <!-- Message si aucun créneau -->
          <div v-else-if="form.date && form.caregiver_id" class="bg-amber-50 border border-amber-200 text-amber-700 px-4 py-3 rounded-lg text-sm">
             Aucun créneau disponible pour cette date. Sélectionnez une autre date.
          </div>
          
          <!-- Message si pas de date ou médecin -->
          <div v-else class="bg-gray-50 border border-gray-200 text-gray-500 px-4 py-3 rounded-lg text-sm">
            Sélectionnez un médecin et une date pour voir les créneaux disponibles
          </div>
        </div>

        <!-- 4. Motif -->
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Motif de la consultation</label>
          <textarea 
            v-model="form.reason" 
            rows="2" 
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" 
            placeholder="Décrivez brièvement le motif de votre consultation..."
          ></textarea>
        </div>
      </div>

      <!-- Résumé -->
      <div v-if="canSubmit" class="bg-rose-50 rounded-lg p-4 border border-rose-200">
        <h4 class="font-medium text-gray-800 text-sm mb-2">📋 Récapitulatif</h4>
        <div class="grid grid-cols-2 gap-2 text-sm">
          <span class="text-gray-500">Médecin :</span>
          <span class="text-gray-800 font-medium">{{ getDoctorName }}</span>
          <span class="text-gray-500">Date :</span>
          <span class="text-gray-800 font-medium">{{ formatDate(form.date) }}</span>
          <span class="text-gray-500">Heure :</span>
          <span class="text-gray-800 font-medium">{{ form.time_slot }}</span>
          <span class="text-gray-500">Durée :</span>
          <span class="text-gray-800 font-medium">{{ getDurationLabel }}</span>
          <span class="text-gray-500">Grossesse :</span>
          <span class="text-gray-800 font-medium">#{{ activePregnancy?.id || 'N/A' }}</span>
        </div>
      </div>

      <!-- Boutons -->
      <div class="flex gap-3 pt-4 border-t border-rose-50">
        <button 
          type="submit" 
          class="flex-1 bg-rose-500 text-white px-6 py-2.5 rounded-lg hover:bg-rose-600 transition font-medium flex items-center justify-center gap-2" 
          :disabled="loading || !canSubmit"
        >
          <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
          {{ loading ? 'Enregistrement...' : 'Confirmer le rendez-vous' }}
        </button>
        <button 
          type="button" 
          @click="$router.back()" 
          class="px-6 py-2.5 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
        >
          Annuler
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft, Loader2, Baby } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'AppointmentCreateView',
  components: { ArrowLeft, Loader2, Baby },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');
    
    const doctors = ref([]);
    const activePregnancy = ref(null);
    const availableSlots = ref([]);
    
    // Dates
    const minDate = computed(() => {
      const today = new Date();
      return today.toISOString().split('T')[0];
    });
    
    const maxDate = computed(() => {
      const date = new Date();
      date.setDate(date.getDate() + 30); // 30 jours max
      return date.toISOString().split('T')[0];
    });

    const form = ref({ 
      caregiver_id: '', 
      date: '', 
      time_slot: '',
      reason: '' 
    });

    const getDoctorName = computed(() => {
      const doctor = doctors.value.find(d => d.id === form.value.caregiver_id);
      return doctor ? doctor.name : '';
    });

    const getDurationLabel = computed(() => {
      const doctor = doctors.value.find(d => d.id === form.value.caregiver_id);
      return doctor?.default_duration || '30 minutes';
    });

    const activePregnancyWeek = computed(() => {
      if (!activePregnancy.value?.start_date) return 0;
      const start = new Date(activePregnancy.value.start_date);
      const now = new Date();
      const diff = Math.floor((now - start) / (1000 * 60 * 60 * 24 * 7));
      return Math.min(diff + 1, 42);
    });

    const canSubmit = computed(() => {
      return form.value.caregiver_id && 
             form.value.date && 
             form.value.time_slot &&
             activePregnancy.value;
    });

    // Charger les médecins
    const loadDoctors = async () => {
      try {
        // TODO: Appel API réel
        // const response = await api.get('/users?role=SOIGNANT');
        // doctors.value = response.data.data;
        
        doctors.value = [
          { id: 1, name: 'Dr. Martin', speciality: 'Gynécologie', default_duration: '30 min' },
          { id: 2, name: 'Dr. Diallo', speciality: 'Obstétrique', default_duration: '45 min' }
        ];
      } catch (error) {
        console.error('Erreur chargement médecins:', error);
      }
    };

    // Charger la grossesse active
    const loadActivePregnancy = async () => {
      try {
        const response = await api.get('/patient/pregnancies');
        let pregnancies = [];
        
        if (response.data && response.data.data) {
          pregnancies = response.data.data;
        } else if (Array.isArray(response.data)) {
          pregnancies = response.data;
        }
        
        // Trouver la grossesse active
        activePregnancy.value = pregnancies.find(p => p.is_active === true) || pregnancies[0] || null;
        
        if (!activePregnancy.value) {
          errorMessage.value = ' Aucune grossesse active. Créez d\'abord une grossesse.';
        }
      } catch (error) {
        console.error('Erreur chargement grossesse:', error);
      }
    };

    // Générer les créneaux disponibles
    const generateSlots = async () => {
      if (!form.value.caregiver_id || !form.value.date) {
        availableSlots.value = [];
        return;
      }

      try {
        // TODO: Appel API pour récupérer les créneaux du médecin
        // const response = await api.get('/appointments/slots', {
        //   params: {
        //     caregiver_id: form.value.caregiver_id,
        //     date: form.value.date
        //   }
        // });
        // availableSlots.value = response.data.data;
        
        // Simulation : créneaux de 9h à 17h (tranches de 30 min)
        const slots = [];
        const startHour = 9;
        const endHour = 17;
        const interval = 30; // minutes
        
        for (let h = startHour; h < endHour; h++) {
          for (let m = 0; m < 60; m += interval) {
            const hourStr = String(h).padStart(2, '0');
            const minStr = String(m).padStart(2, '0');
            slots.push(`${hourStr}:${minStr}`);
          }
        }
        
        // Simuler des créneaux déjà pris (aléatoire)
        const takenSlots = ['09:00', '10:00', '14:30', '15:30'];
        availableSlots.value = slots.filter(slot => !takenSlots.includes(slot));
        
        // Réinitialiser le créneau sélectionné
        form.value.time_slot = '';
        
      } catch (error) {
        console.error('Erreur génération créneaux:', error);
        availableSlots.value = [];
      }
    };

    const selectSlot = (slot) => {
      form.value.time_slot = slot;
    };

    const handleSubmit = async () => {
      // Validation
      if (!form.value.caregiver_id) {
        errorMessage.value = 'Veuillez sélectionner un médecin';
        return;
      }
      if (!form.value.date) {
        errorMessage.value = 'Veuillez sélectionner une date';
        return;
      }
      if (!form.value.time_slot) {
        errorMessage.value = 'Veuillez sélectionner un créneau horaire';
        return;
      }
      if (!activePregnancy.value) {
        errorMessage.value = 'Aucune grossesse active. Créez d\'abord une grossesse.';
        return;
      }

      loading.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      try {
        const dateTime = `${form.value.date}T${form.value.time_slot}:00`;
        
        const payload = {
          caregiver: form.value.caregiver_id,
          pregnancy: activePregnancy.value.id,
          date_time: dateTime,
          duration_minutes: 30,
          reason: form.value.reason || 'Consultation de suivi'
        };
        
        console.log('📤 Création rendez-vous:', payload);
        
        const response = await api.post('/patient/appointments', payload);
        console.log('📥 Réponse:', response.data);
        
        if (response.data && response.data.message) {
          successMessage.value = response.data.message || ' Rendez-vous pris avec succès !';
        }
        
        setTimeout(() => {
          router.push('/app/patient/appointments');
        }, 1500);
        
      } catch (error) {
        console.error(' Erreur création rendez-vous:', error);
        
        if (error.response?.data?.message) {
          errorMessage.value = error.response.data.message;
        } else if (error.response?.data?.errors) {
          const errors = error.response.data.errors;
          const firstError = Object.values(errors)[0];
          errorMessage.value = Array.isArray(firstError) ? firstError[0] : 'Erreur de validation';
        } else {
          errorMessage.value = 'Erreur lors de la prise de rendez-vous';
        }
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadDoctors();
      loadActivePregnancy();
    });

    return { 
      form, 
      loading, 
      errorMessage, 
      successMessage, 
      doctors, 
      activePregnancy,
      activePregnancyWeek,
      availableSlots,
      minDate,
      maxDate,
      getDoctorName,
      getDurationLabel,
      canSubmit,
      formatDate, 
      generateSlots,
      selectSlot,
      handleSubmit 
    };
  }
};
</script>