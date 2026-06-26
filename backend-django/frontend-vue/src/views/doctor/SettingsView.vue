<!-- src/views/doctor/SettingsView.vue -->
<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Paramètres</h1>
      <p class="text-gray-500 text-sm">Gérez vos préférences et paramètres</p>
    </div>

    <div class="space-y-4">
      <!-- Notifications -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-blue-100">
        <h3 class="font-semibold text-gray-800 mb-4"> Notifications</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-700">Rappels de rendez-vous</p>
              <p class="text-sm text-gray-500">Recevoir un rappel 24h avant chaque rendez-vous</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.reminders" class="sr-only peer" />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-700">Notifications email</p>
              <p class="text-sm text-gray-500">Recevoir les notifications par email</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="settings.email" class="sr-only peer" />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Sécurité -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-blue-100">
        <h3 class="font-semibold text-gray-800 mb-4"> Sécurité</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Changer le mot de passe</label>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <input v-model="password.current" type="password" placeholder="Mot de passe actuel" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" />
              <input v-model="password.new" type="password" placeholder="Nouveau mot de passe" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" />
              <input v-model="password.confirm" type="password" placeholder="Confirmer le mot de passe" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400" />
            </div>
            <button @click="changePassword" class="mt-3 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition text-sm">
              Mettre à jour le mot de passe
            </button>
            <p v-if="passwordError" class="text-red-500 text-sm mt-2">{{ passwordError }}</p>
            <p v-if="passwordSuccess" class="text-green-500 text-sm mt-2">{{ passwordSuccess }}</p>
          </div>
        </div>
      </div>

      <!-- Langue -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-blue-100">
        <h3 class="font-semibold text-gray-800 mb-4"> Langue</h3>
        <select v-model="settings.language" class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400">
          <option value="fr">Français</option>
          <option value="en">English</option>
        </select>
      </div>

      <!-- Sauvegarde -->
      <div class="flex gap-3">
        <button @click="saveSettings" class="bg-blue-500 text-white px-6 py-2.5 rounded-lg hover:bg-blue-600 transition font-medium" :disabled="saving">
          <Loader2 v-if="saving" class="w-4 h-4 animate-spin inline mr-2" />
          {{ saving ? 'Enregistrement...' : ' Enregistrer les paramètres' }}
        </button>
        <button @click="resetSettings" class="px-6 py-2.5 border border-gray-200 rounded-lg hover:bg-gray-50 transition">
          Réinitialiser
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Loader2 } from 'lucide-vue-next';

export default {
  name: 'DoctorSettingsView',
  components: { Loader2 },
  setup() {
    const saving = ref(false);
    const passwordError = ref('');
    const passwordSuccess = ref('');

    const settings = ref({
      reminders: true,
      email: true,
      language: 'fr'
    });

    const password = ref({
      current: '',
      new: '',
      confirm: ''
    });

    const saveSettings = async () => {
      saving.value = true;
      try {
        // Sauvegarder les paramètres
        console.log('📤 Sauvegarde paramètres:', settings.value);
        // await api.put('/doctor/settings', settings.value);
        alert(' Paramètres enregistrés !');
      } catch (err) {
        console.error(' Erreur:', err);
        alert(' Erreur lors de la sauvegarde');
      } finally {
        saving.value = false;
      }
    };

    const changePassword = async () => {
      if (!password.value.current || !password.value.new || !password.value.confirm) {
        passwordError.value = 'Tous les champs sont requis';
        return;
      }
      if (password.value.new !== password.value.confirm) {
        passwordError.value = 'Les mots de passe ne correspondent pas';
        return;
      }
      if (password.value.new.length < 8) {
        passwordError.value = 'Le mot de passe doit contenir au moins 8 caractères';
        return;
      }

      try {
        // await api.post('/auth/change-password', {
        //   current: password.value.current,
        //   new: password.value.new
        // });
        passwordError.value = '';
        passwordSuccess.value = ' Mot de passe mis à jour avec succès !';
        password.value = { current: '', new: '', confirm: '' };
        
        setTimeout(() => {
          passwordSuccess.value = '';
        }, 3000);
      } catch (err) {
        console.error(' Erreur:', err);
        passwordError.value = err.response?.data?.message || 'Erreur lors du changement de mot de passe';
      }
    };

    const resetSettings = () => {
      if (!confirm('Réinitialiser tous les paramètres ?')) return;
      settings.value = {
        reminders: true,
        email: true,
        language: 'fr'
      };
    };

    return {
      settings,
      password,
      saving,
      passwordError,
      passwordSuccess,
      saveSettings,
      changePassword,
      resetSettings
    };
  }
};
</script>