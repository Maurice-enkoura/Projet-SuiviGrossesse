<!-- src/views/patient/ProfileView.vue -->
<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- En-tête -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 flex items-center gap-4">
      <div class="w-20 h-20 bg-gradient-to-r from-rose-400 to-rose-600 rounded-full flex items-center justify-center text-white text-3xl font-bold">
        {{ initials }}
      </div>
      <div>
        <h1 class="text-2xl font-bold text-gray-800">{{ user?.username || user?.name || 'Utilisateur' }}</h1>
        <p class="text-gray-500">{{ user?.email }}</p>
        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs" :class="user?.is_active ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'">
          <CheckCircle class="w-3 h-3" /> {{ user?.is_active ? 'Compte actif' : 'Compte en attente' }}
        </span>
        <span v-if="user?.role === 'SOIGNANT'" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-blue-100 text-blue-700 ml-2">
          <User class="w-3 h-3" /> {{ user?.speciality || 'Médecin' }}
        </span>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-rose-500 text-sm">Grossesses</p>
        <p class="text-2xl font-bold text-gray-800">{{ stats.pregnancies }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-green-500 text-sm">Rendez-vous</p>
        <p class="text-2xl font-bold text-green-600">{{ stats.appointments }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
        <p class="text-purple-500 text-sm">Membre depuis</p>
        <p class="text-2xl font-bold text-purple-600">{{ formatDate(user?.created_at) }}</p>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement du profil...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Message de succès -->
    <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
       {{ successMessage }}
    </div>

    <!-- Formulaire -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
      <h2 class="text-lg font-bold text-gray-800 mb-4"> Mes informations</h2>
      <form @submit.prevent="updateProfile" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nom d'utilisateur</label>
            <input v-model="form.username" type="text" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" disabled />
            <p class="text-xs text-gray-400 mt-1">Le nom d'utilisateur ne peut pas être modifié</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="form.email" type="email" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" disabled />
            <p class="text-xs text-gray-400 mt-1">L'email ne peut pas être modifié</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
            <input v-model="form.phone" type="tel" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" placeholder="+242 06 123 45 67" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Date de naissance</label>
            <input v-model="form.date_of_birth" type="date" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Adresse</label>
            <textarea v-model="form.address" rows="2" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" placeholder="Votre adresse"></textarea>
          </div>
        </div>
        <div class="flex gap-3 pt-4 border-t border-rose-50">
          <button type="submit" class="bg-rose-500 text-white px-6 py-2 rounded-lg hover:bg-rose-600 transition disabled:opacity-50 flex items-center gap-2" :disabled="saving">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <Save v-else class="w-4 h-4" />
            {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
          <button type="button" @click="resetForm" class="px-6 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition">Annuler</button>
        </div>
      </form>
    </div>

    <!-- Sécurité -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
      <h2 class="text-lg font-bold text-gray-800 mb-4"> Sécurité</h2>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="font-medium text-gray-800">Mot de passe</p>
            <p class="text-sm text-gray-500">Dernière mise à jour : {{ passwordUpdated || 'Jamais' }}</p>
          </div>
          <button @click="showPasswordModal = true" class="text-rose-500 hover:underline text-sm">Modifier</button>
        </div>
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="font-medium text-gray-800">Statut du compte</p>
            <p class="text-sm" :class="user?.account_status === 'ACTIVE' ? 'text-green-600' : 'text-yellow-600'">
              {{ getStatusLabel(user?.account_status) }}
            </p>
          </div>
          <span class="px-2 py-1 rounded-full text-xs font-medium" :class="getStatusClass(user?.account_status)">
            {{ getStatusLabel(user?.account_status) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Modal de changement de mot de passe -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-md w-full p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold text-gray-800"> Changer le mot de passe</h2>
          <button @click="showPasswordModal = false" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        
        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Mot de passe actuel *</label>
            <input v-model="passwordForm.current" type="password" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nouveau mot de passe *</label>
            <input v-model="passwordForm.new" type="password" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" required />
            <p class="text-xs text-gray-400 mt-1">Minimum 8 caractères</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirmer le mot de passe *</label>
            <input v-model="passwordForm.confirm" type="password" class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" required />
          </div>
          
          <div v-if="passwordError" class="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg text-sm">
             {{ passwordError }}
          </div>
          <div v-if="passwordSuccess" class="bg-green-50 border border-green-200 text-green-700 px-3 py-2 rounded-lg text-sm">
             {{ passwordSuccess }}
          </div>
          
          <div class="flex gap-3 pt-4 border-t">
            <button type="submit" class="flex-1 bg-rose-500 text-white px-6 py-2 rounded-lg hover:bg-rose-600 transition disabled:opacity-50 flex items-center justify-center gap-2" :disabled="passwordSaving">
              <Loader2 v-if="passwordSaving" class="w-4 h-4 animate-spin" />
              {{ passwordSaving ? 'Modification...' : 'Modifier' }}
            </button>
            <button type="button" @click="showPasswordModal = false" class="px-6 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { CheckCircle, Save, User, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'ProfileView',
  components: { CheckCircle, Save, User, Loader2 },
  setup() {
    const authStore = useAuthStore();
    const user = computed(() => authStore.user);
    
    const loading = ref(true);
    const saving = ref(false);
    const passwordSaving = ref(false);
    const error = ref('');
    const successMessage = ref('');
    const passwordError = ref('');
    const passwordSuccess = ref('');
    const showPasswordModal = ref(false);
    const passwordUpdated = ref('Jamais');

    const form = ref({
      username: '',
      email: '',
      phone: '',
      date_of_birth: '',
      address: ''
    });

    const passwordForm = ref({
      current: '',
      new: '',
      confirm: ''
    });

    const stats = ref({
      pregnancies: 0,
      appointments: 0
    });

    const initials = computed(() => {
      const name = user.value?.username || user.value?.name || 'U';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    });

    const getStatusClass = (status) => {
      const classes = {
        'ACTIVE': 'bg-green-100 text-green-700',
        'PENDING': 'bg-yellow-100 text-yellow-700',
        'REJECTED': 'bg-red-100 text-red-700',
        'SUSPENDED': 'bg-gray-100 text-gray-700'
      };
      return classes[status] || 'bg-gray-100 text-gray-700';
    };

    const getStatusLabel = (status) => {
      const labels = {
        'ACTIVE': ' Actif',
        'PENDING': ' En attente de validation',
        'REJECTED': ' Rejeté',
        'SUSPENDED': ' Suspendu'
      };
      return labels[status] || status;
    };

    const resetForm = () => {
      const userData = user.value || {};
      form.value = {
        username: userData.username || '',
        email: userData.email || '',
        phone: userData.phone || '',
        date_of_birth: userData.date_of_birth || '',
        address: userData.address || ''
      };
    };

    const loadProfile = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        // Récupérer les informations du profil
        const response = await api.get('/auth/me');
        console.log('📥 Profil:', response.data);
        
        if (response.data && response.data.user) {
          authStore.setUser(response.data.user);
          resetForm();
        }
        
        // Récupérer les statistiques
        // 1. Grossesses
        const pregRes = await api.get('/patient/pregnancies');
        if (pregRes.data && pregRes.data.data) {
          stats.value.pregnancies = pregRes.data.data.length;
        }
        
        // 2. Rendez-vous
        const apptRes = await api.get('/patient/appointments');
        if (apptRes.data && apptRes.data.data) {
          stats.value.appointments = apptRes.data.data.length;
        }
        
      } catch (err) {
        console.error(' Erreur chargement profil:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    const updateProfile = async () => {
      saving.value = true;
      error.value = '';
      successMessage.value = '';
      
      try {
        const payload = {
          phone: form.value.phone,
          date_of_birth: form.value.date_of_birth,
          address: form.value.address
        };
        
        console.log('📤 Mise à jour profil:', payload);
        
        const response = await api.put('/auth/me', payload);
        console.log('📥 Réponse:', response.data);
        
        if (response.data && response.data.user) {
          authStore.updateUser(response.data.user);
          successMessage.value = ' Profil mis à jour avec succès !';
          setTimeout(() => { successMessage.value = ''; }, 3000);
        }
        
      } catch (err) {
        console.error(' Erreur mise à jour:', err);
        error.value = err.response?.data?.message || 'Erreur lors de la mise à jour';
      } finally {
        saving.value = false;
      }
    };

    const changePassword = async () => {
      // Validation
      if (!passwordForm.value.current || !passwordForm.value.new || !passwordForm.value.confirm) {
        passwordError.value = 'Tous les champs sont requis';
        return;
      }
      if (passwordForm.value.new !== passwordForm.value.confirm) {
        passwordError.value = 'Les mots de passe ne correspondent pas';
        return;
      }
      if (passwordForm.value.new.length < 8) {
        passwordError.value = 'Le mot de passe doit contenir au moins 8 caractères';
        return;
      }

      passwordSaving.value = true;
      passwordError.value = '';
      passwordSuccess.value = '';
      
      try {
        const response = await api.post('/auth/change-password', {
          current_password: passwordForm.value.current,
          new_password: passwordForm.value.new
        });
        
        console.log('📥 Mot de passe modifié:', response.data);
        
        passwordSuccess.value = ' Mot de passe modifié avec succès !';
        passwordUpdated.value = new Date().toLocaleDateString('fr-FR');
        passwordForm.value = { current: '', new: '', confirm: '' };
        
        setTimeout(() => {
          passwordSuccess.value = '';
          showPasswordModal.value = false;
        }, 2000);
        
      } catch (err) {
        console.error(' Erreur changement mot de passe:', err);
        passwordError.value = err.response?.data?.message || 'Erreur lors du changement de mot de passe';
      } finally {
        passwordSaving.value = false;
      }
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      user,
      form,
      stats,
      loading,
      saving,
      passwordSaving,
      error,
      successMessage,
      passwordError,
      passwordSuccess,
      initials,
      passwordUpdated,
      showPasswordModal,
      passwordForm,
      formatDate,
      getStatusClass,
      getStatusLabel,
      resetForm,
      updateProfile,
      changePassword
    };
  }
};
</script>