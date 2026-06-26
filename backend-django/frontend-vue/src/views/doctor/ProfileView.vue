<!-- src/views/doctor/ProfileView.vue -->
<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Mon profil</h1>
      <p class="text-gray-500 text-sm">Gérez vos informations personnelles</p>
    </div>

    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-blue-100">
      <Loader2 class="w-12 h-12 text-blue-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement...</p>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <form v-else @submit.prevent="handleSubmit" class="bg-white rounded-xl p-6 shadow-sm border border-blue-100 space-y-5">
      <!-- Message de succès -->
      <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
         {{ successMessage }}
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nom d'utilisateur</label>
          <input v-model="form.username" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" disabled />
          <p class="text-xs text-gray-400 mt-1">Le nom d'utilisateur ne peut pas être modifié</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" disabled />
          <p class="text-xs text-gray-400 mt-1">L'email ne peut pas être modifié</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Spécialité</label>
          <input v-model="form.speciality" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" placeholder="Gynécologie, Obstétrique..." />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
          <input v-model="form.phone" type="tel" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" placeholder="+242 06 123 45 67" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Date de naissance</label>
          <input v-model="form.date_of_birth" type="date" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" />
        </div>
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Adresse</label>
          <textarea v-model="form.address" rows="2" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" placeholder="Votre adresse professionnelle"></textarea>
        </div>
      </div>

      <div class="border-t border-blue-50 pt-4">
        <button type="submit" class="bg-blue-500 text-white px-6 py-2.5 rounded-lg hover:bg-blue-600 transition font-medium" :disabled="saving">
          <Loader2 v-if="saving" class="w-4 h-4 animate-spin inline mr-2" />
          {{ saving ? 'Enregistrement...' : '  Mettre à jour' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { Loader2 } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'DoctorProfileView',
  components: { Loader2 },
  setup() {
    const authStore = useAuthStore();
    const loading = ref(true);
    const saving = ref(false);
    const error = ref('');
    const successMessage = ref('');

    const form = ref({
      username: '',
      email: '',
      speciality: '',
      phone: '',
      date_of_birth: '',
      address: ''
    });

    const loadProfile = async () => {
      loading.value = true;
      try {
        // Récupérer les informations depuis le store ou l'API
        const user = authStore.user;
        if (user) {
          form.value.username = user.username || '';
          form.value.email = user.email || '';
          form.value.speciality = user.speciality || '';
          form.value.phone = user.phone || '';
          form.value.date_of_birth = user.date_of_birth || '';
          form.value.address = user.address || '';
        }
      } catch (err) {
        console.error(' Erreur chargement profil:', err);
        error.value = 'Erreur lors du chargement du profil';
      } finally {
        loading.value = false;
      }
    };

    const handleSubmit = async () => {
      saving.value = true;
      error.value = '';
      successMessage.value = '';

      try {
        // Envoyer les modifications
        await api.put('/auth/me', form.value);
        successMessage.value = ' Profil mis à jour avec succès !';
        
        // Mettre à jour le store
        authStore.updateUser(form.value);
        
        setTimeout(() => {
          successMessage.value = '';
        }, 3000);
      } catch (err) {
        console.error(' Erreur mise à jour:', err);
        error.value = err.response?.data?.message || 'Erreur lors de la mise à jour';
      } finally {
        saving.value = false;
      }
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      form,
      loading,
      saving,
      error,
      successMessage,
      handleSubmit
    };
  }
};
</script>