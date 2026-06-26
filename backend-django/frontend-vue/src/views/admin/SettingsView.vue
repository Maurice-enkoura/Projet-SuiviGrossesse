<!-- src/views/admin/SettingsView.vue -->
<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Paramètres système</h1>
      <p class="text-gray-500 text-sm">Configurez les paramètres de la plateforme</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-purple-100">
      <Loader2 class="w-12 h-12 text-purple-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des paramètres...</p>
    </div>

    <!-- Message de succès -->
    <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
       {{ success }}
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Formulaire -->
    <form v-else @submit.prevent="saveSettings" class="space-y-6">
      <!-- Général -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-purple-100">
        <h2 class="font-bold text-gray-800 mb-4"> Général</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nom de la plateforme</label>
            <input 
              v-model="settings.app_name" 
              type="text" 
              class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-100" 
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email de contact</label>
            <input 
              v-model="settings.contact_email" 
              type="email" 
              class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-100" 
              required
            />
          </div>
        </div>
      </div>

      <!-- Sécurité -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-purple-100">
        <h2 class="font-bold text-gray-800 mb-4"> Sécurité</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Durée de session (minutes)</label>
            <input 
              v-model="settings.session_timeout" 
              type="number" 
              min="15"
              max="1440"
              class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-100" 
              required
            />
            <p class="text-xs text-gray-400 mt-1">Entre 15 et 1440 minutes (24h)</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tentatives de connexion max</label>
            <input 
              v-model="settings.max_attempts" 
              type="number" 
              min="3"
              max="10"
              class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-100" 
              required
            />
            <p class="text-xs text-gray-400 mt-1">Entre 3 et 10 tentatives</p>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="bg-white rounded-xl p-6 shadow-sm border border-purple-100">
        <h2 class="font-bold text-gray-800 mb-4"> Notifications</h2>
        <div class="space-y-3">
          <div v-for="notif in notificationSettings" :key="notif.key" class="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
            <div>
              <p class="font-medium text-gray-800">{{ notif.label }}</p>
              <p class="text-sm text-gray-500">{{ notif.description }}</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notif.enabled" class="sr-only peer" />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Boutons -->
      <div class="flex gap-3">
        <button 
          type="submit" 
          class="bg-purple-500 text-white px-6 py-2.5 rounded-lg hover:bg-purple-600 transition font-medium flex items-center gap-2 disabled:opacity-50" 
          :disabled="saving"
        >
          <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
          {{ saving ? 'Enregistrement...' : ' Enregistrer' }}
        </button>
        <button 
          type="button" 
          @click="resetSettings" 
          class="px-6 py-2.5 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
        >
          Réinitialiser
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Loader2 } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'AdminSettingsView',
  components: { Loader2 },
  setup() {
    const loading = ref(true);
    const saving = ref(false);
    const error = ref('');
    const success = ref('');

    const settings = ref({
      app_name: 'Suivi Grossesse',
      contact_email: 'contact@suivi-grossesse.com',
      session_timeout: 60,
      max_attempts: 5
    });

    const notificationSettings = ref([
      { key: 'email', label: ' Emails de notification', description: 'Recevoir les notifications par email', enabled: true },
      { key: 'sms', label: ' SMS de rappel', description: 'Envoyer des SMS pour les rendez-vous', enabled: false },
      { key: 'push', label: ' Notifications push', description: 'Notifications sur le navigateur', enabled: false }
    ]);

    const loadSettings = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        //  Récupérer les paramètres depuis l'API
        const response = await api.get('/admin/settings');
        console.log('📥 Paramètres récupérés:', response.data);
        
        if (response.data && response.data.data) {
          const data = response.data.data;
          
          // Mettre à jour les paramètres
          settings.value = {
            app_name: data.app_name || 'Suivi Grossesse',
            contact_email: data.contact_email || 'contact@suivi-grossesse.com',
            session_timeout: data.session_timeout || 60,
            max_attempts: data.max_attempts || 5
          };
          
          // Mettre à jour les notifications
          if (data.notifications) {
            notificationSettings.value = notificationSettings.value.map(notif => ({
              ...notif,
              enabled: data.notifications[notif.key] !== undefined ? data.notifications[notif.key] : notif.enabled
            }));
          }
        }
      } catch (err) {
        console.error(' Erreur chargement paramètres:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement des paramètres';
        
        // En cas d'erreur, on garde les valeurs par défaut
        // Les paramètres par défaut sont déjà définis
      } finally {
        loading.value = false;
      }
    };

    const saveSettings = async () => {
      saving.value = true;
      error.value = '';
      success.value = '';
      
      try {
        //  Sauvegarder les paramètres
        const payload = {
          app_name: settings.value.app_name,
          contact_email: settings.value.contact_email,
          session_timeout: parseInt(settings.value.session_timeout),
          max_attempts: parseInt(settings.value.max_attempts),
          notifications: notificationSettings.value.reduce((acc, notif) => {
            acc[notif.key] = notif.enabled;
            return acc;
          }, {})
        };
        
        console.log(' Sauvegarde des paramètres:', payload);
        
        const response = await api.put('/admin/settings', payload);
        console.log(' Réponse sauvegarde:', response.data);
        
        success.value = ' Paramètres enregistrés avec succès !';
        setTimeout(() => { success.value = ''; }, 3000);
        
      } catch (err) {
        console.error(' Erreur sauvegarde:', err);
        error.value = err.response?.data?.message || 'Erreur lors de la sauvegarde des paramètres';
      } finally {
        saving.value = false;
      }
    };

    const resetSettings = () => {
      if (!confirm('Réinitialiser tous les paramètres ?')) return;
      
      settings.value = {
        app_name: 'Suivi Grossesse',
        contact_email: 'contact@suivi-grossesse.com',
        session_timeout: 60,
        max_attempts: 5
      };
      
      notificationSettings.value = [
        { key: 'email', label: ' Emails de notification', description: 'Recevoir les notifications par email', enabled: true },
        { key: 'sms', label: '📱 SMS de rappel', description: 'Envoyer des SMS pour les rendez-vous', enabled: false },
        { key: 'push', label: ' Notifications push', description: 'Notifications sur le navigateur', enabled: false }
      ];
      
      // Sauvegarder les paramètres par défaut
      saveSettings();
    };

    onMounted(() => {
      loadSettings();
    });

    return {
      loading,
      saving,
      error,
      success,
      settings,
      notificationSettings,
      saveSettings,
      resetSettings
    };
  }
};
</script>