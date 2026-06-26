<!-- src/views/patient/PregnancyCreateView.vue -->
<template>
  <div class="max-w-2xl mx-auto">
    <div class="flex items-center gap-3 mb-6">
      <button @click="$router.back()" class="p-2 rounded-lg hover:bg-rose-50 transition">
        <ArrowLeft class="w-5 h-5 text-gray-600" />
      </button>
      <h1 class="text-2xl font-bold text-gray-800">➕ Nouvelle grossesse</h1>
    </div>

    <form @submit.prevent="handleSubmit" class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 space-y-5">
      <!-- Message d'erreur -->
      <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
        ❌ {{ errorMessage }}
      </div>

      <!-- Message de succès -->
      <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
        ✅ {{ successMessage }}
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date de début *</label>
          <input 
            v-model="form.start_date" 
            type="date" 
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition" 
            required 
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date prévue d'accouchement</label>
          <input 
            v-model="form.expected_delivery_date" 
            type="date" 
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition" 
          />
        </div>
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
          <textarea 
            v-model="form.notes" 
            rows="3" 
            class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition" 
            placeholder="Informations complémentaires..."
          ></textarea>
        </div>
      </div>

      <div class="flex gap-3 pt-4 border-t border-rose-50">
        <button 
          type="submit" 
          class="flex-1 bg-rose-500 text-white px-6 py-2.5 rounded-lg hover:bg-rose-600 transition font-medium flex items-center justify-center gap-2"
          :disabled="loading"
        >
          <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
          {{ loading ? 'Enregistrement...' : 'Enregistrer' }}
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft, Loader2 } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'PregnancyCreateView',
  components: { ArrowLeft, Loader2 },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');
    
    const form = ref({ 
      start_date: '', 
      expected_delivery_date: '', 
      notes: '' 
    });

    const handleSubmit = async () => {
      // Validation
      if (!form.value.start_date) {
        errorMessage.value = 'Veuillez renseigner la date de début';
        return;
      }

      loading.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      try {
        console.log('📤 Création grossesse:', form.value);
        
        const response = await api.post('/patient/pregnancies', {
          start_date: form.value.start_date,
          expected_delivery_date: form.value.expected_delivery_date || null,
          notes: form.value.notes || ''
        });

        console.log('📥 Réponse brute:', response.data);
        
        // ✅ Vos APIs retournent { message, data }
        if (response.data && response.data.message) {
          successMessage.value = response.data.message || '✅ Grossesse créée avec succès !';
        }
        
        // ✅ Si l'API retourne les données de la grossesse créée
        if (response.data && response.data.data) {
          console.log('✅ Grossesse créée:', response.data.data);
        }
        
        // Rediriger après un délai
        setTimeout(() => {
          router.push('/app/patient/pregnancies');
        }, 1500);
        
      } catch (error) {
        console.error('❌ Erreur création:', error);
        
        if (error.response?.data?.message) {
          errorMessage.value = error.response.data.message;
        } else if (error.response?.data?.errors) {
          const errors = error.response.data.errors;
          const firstError = Object.values(errors)[0];
          errorMessage.value = Array.isArray(firstError) ? firstError[0] : 'Erreur de validation';
        } else if (error.response?.status === 400) {
          errorMessage.value = 'Vous avez déjà une grossesse active.';
        } else if (error.response?.status === 422) {
          errorMessage.value = 'Données invalides. Vérifiez les champs.';
        } else {
          errorMessage.value = 'Erreur lors de la création de la grossesse.';
        }
      } finally {
        loading.value = false;
      }
    };

    return { form, loading, errorMessage, successMessage, handleSubmit };
  }
};
</script>