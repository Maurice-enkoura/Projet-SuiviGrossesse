<!-- src/views/admin/StatsView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Statistiques globales</h1>
      <p class="text-gray-500 text-sm">Vue d'ensemble de la plateforme</p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-purple-100">
      <Loader2 class="w-12 h-12 text-purple-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des statistiques...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Debug - Afficher les données reçues -->
    <div v-if="debug" class="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded-lg text-sm">
      <p class="font-medium">🔍 Données reçues :</p>
      <pre class="text-xs mt-1 overflow-auto max-h-32">{{ JSON.stringify(stats, null, 2) }}</pre>
    </div>

    <!-- Cartes -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-xl p-4 shadow-sm border border-purple-100">
        <p class="text-gray-500 text-xs font-medium">Total utilisateurs</p>
        <p class="text-2xl font-bold text-gray-800">{{ stats?.users?.total || 0 }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-green-100">
        <p class="text-gray-500 text-xs font-medium">Grossesses actives</p>
        <p class="text-2xl font-bold text-green-600">{{ stats?.pregnancies?.active || 0 }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-blue-100">
        <p class="text-gray-500 text-xs font-medium">Rendez-vous</p>
        <p class="text-2xl font-bold text-blue-600">{{ stats?.appointments?.total || 0 }}</p>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-amber-100">
        <p class="text-gray-500 text-xs font-medium">Consultations</p>
        <p class="text-2xl font-bold text-amber-600">{{ stats?.consultations?.total || 0 }}</p>
      </div>
    </div>

    <!-- Détails -->
    <div class="bg-white rounded-xl shadow-sm border border-purple-100 overflow-hidden">
      <div class="px-6 py-4 border-b border-purple-50">
        <h3 class="font-semibold text-gray-800"> Détails des statistiques</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-purple-50 border-b border-purple-100">
            <tr>
              <th class="text-left py-3 px-4 text-xs font-semibold text-gray-500">Catégorie</th>
              <th class="text-right py-3 px-4 text-xs font-semibold text-gray-500">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Total utilisateurs</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.users?.total || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Patients</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.users?.patients || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Médecins</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.users?.caregivers || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Total grossesses</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.pregnancies?.total || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Grossesses actives</td>
              <td class="py-3 px-4 text-right font-bold text-green-600">{{ stats?.pregnancies?.active || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Total rendez-vous</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.appointments?.total || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Rendez-vous en attente</td>
              <td class="py-3 px-4 text-right font-bold text-amber-600">{{ stats?.appointments?.pending || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Rendez-vous effectués</td>
              <td class="py-3 px-4 text-right font-bold text-green-600">{{ stats?.appointments?.completed || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Total consultations</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.consultations?.total || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Total examens</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.exams?.total || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Total alertes</td>
              <td class="py-3 px-4 text-right font-bold text-gray-800">{{ stats?.alerts?.total || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Alertes actives</td>
              <td class="py-3 px-4 text-right font-bold text-amber-600">{{ stats?.alerts?.active || 0 }}</td>
            </tr>
            <tr class="border-b border-purple-50 hover:bg-purple-50/50 transition">
              <td class="py-3 px-4 font-medium text-gray-800"> Alertes critiques</td>
              <td class="py-3 px-4 text-right font-bold text-red-600">{{ stats?.alerts?.critical || 0 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Loader2 } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'AdminStatsView',
  components: { Loader2 },
  setup() {
    const loading = ref(true);
    const error = ref('');
    const stats = ref({});
    const debug = ref(true); // Mettre à false après avoir vérifié

    const loadStats = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log(' Appel API /admin/stats...');
        const response = await api.get('/admin/stats');
        console.log(' Réponse brute:', response.data);
        
        if (response.data && response.data.data) {
          // ✅ Structure de l'API : data.data.users, data.data.pregnancies, etc.
          stats.value = response.data.data;
          console.log(' Données extraites:', stats.value);
          
          // Afficher quelques valeurs pour vérifier
          console.log(' Total utilisateurs:', stats.value?.users?.total);
          console.log(' Grossesses actives:', stats.value?.pregnancies?.active);
          console.log(' Rendez-vous:', stats.value?.appointments?.total);
        }
        
      } catch (err) {
        console.error(' Erreur chargement stats:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
        // Désactiver le debug après 5 secondes
        setTimeout(() => {
          debug.value = false;
        }, 5000);
      }
    };

    onMounted(() => {
      loadStats();
    });

    return {
      loading,
      error,
      stats,
      debug
    };
  }
};
</script>