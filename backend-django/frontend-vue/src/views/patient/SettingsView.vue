<!-- src/views/patient/SettingsView.vue -->
<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Paramètres</h1>
      <p class="text-gray-500 text-sm">Personnalisez vos préférences</p>
    </div>

    <!-- Notifications -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
      <h2 class="font-bold text-gray-800 mb-4"> Notifications</h2>
      <div class="space-y-3">
        <div v-for="notif in notifications" :key="notif.key" class="flex items-center justify-between p-3 bg-rose-50 rounded-lg">
          <div><p class="font-medium text-gray-800">{{ notif.label }}</p><p class="text-sm text-gray-500">{{ notif.description }}</p></div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" v-model="notif.enabled" class="sr-only peer" />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-rose-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-rose-500"></div>
          </label>
        </div>
      </div>
    </div>

    <!-- Langue -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
      <h2 class="font-bold text-gray-800 mb-4"> Langue</h2>
      <div class="grid grid-cols-2 gap-3">
        <div v-for="lang in languages" :key="lang.code" class="p-3 border rounded-lg cursor-pointer transition" :class="selectedLanguage === lang.code ? 'border-rose-500 bg-rose-50' : 'border-gray-200 hover:border-rose-300'" @click="selectedLanguage = lang.code">
          <div class="flex items-center gap-3"><span class="text-2xl">{{ lang.flag }}</span><div><p class="font-medium">{{ lang.name }}</p><p class="text-xs text-gray-500">{{ lang.native }}</p></div></div>
        </div>
      </div>
    </div>

    <!-- Compte -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
      <h2 class="font-bold text-gray-800 mb-4"> Compte</h2>
      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-rose-50 rounded-lg"><div><p class="font-medium text-gray-800">Supprimer le compte</p><p class="text-sm text-gray-500">Cette action est irréversible</p></div><button @click="deleteAccount" class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition">Supprimer</button></div>
        <div class="flex items-center justify-between p-3 bg-rose-50 rounded-lg"><div><p class="font-medium text-gray-800">Exporter les données</p><p class="text-sm text-gray-500">Téléchargez toutes vos données</p></div><button @click="exportData" class="bg-rose-500 text-white px-4 py-2 rounded-lg hover:bg-rose-600 transition"><Download class="w-4 h-4 inline mr-2" /> Exporter</button></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { Download } from 'lucide-vue-next';

export default {
  name: 'SettingsView',
  components: { Download },
  setup() {
    const selectedLanguage = ref('fr');

    const notifications = ref([
      { key: 'appointments', label: ' Rappels de rendez-vous', description: 'Recevez un rappel 24h avant', enabled: true },
      { key: 'messages', label: ' Nouveaux messages', description: 'Soyez informé des nouveaux messages', enabled: true },
      { key: 'results', label: ' Résultats d\'analyses', description: 'Recevez une notification des résultats', enabled: true },
      { key: 'promotions', label: ' Offres et promotions', description: 'Recevez des offres spéciales', enabled: false }
    ]);

    const languages = [
      { code: 'fr', name: 'Français', native: 'Français', flag: '🇫🇷' },
      { code: 'en', name: 'English', native: 'English', flag: '🇬🇧' }
    ];

    const deleteAccount = () => { if (confirm(' Supprimer le compte ?')) alert(' Compte supprimé'); };
    const exportData = () => alert(' Exportation en cours...');

    return { notifications, languages, selectedLanguage, deleteAccount, exportData };
  }
};
</script>