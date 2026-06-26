<!-- src/views/patient/MedicalRecordsView.vue -->
<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Dossiers médicaux</h1>
        <p class="text-gray-500 text-sm">Consultez vos documents médicaux</p>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Filtres -->
    <div class="bg-white rounded-xl p-4 shadow-sm border border-rose-100">
      <div class="flex flex-wrap gap-3">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder=" Rechercher..." 
          class="flex-1 min-w-[200px] px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" 
        />
        <select 
          v-model="selectedCategory" 
          class="px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
        >
          <option value="">Toutes les catégories</option>
          <option value="Analyse">Analyses</option>
          <option value="Échographie">Échographies</option>
          <option value="Ordonnance">Ordonnances</option>
          <option value="Autre">Autre</option>
        </select>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des dossiers...</p>
    </div>

    <!-- Liste -->
    <div v-else-if="filteredRecords.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="record in filteredRecords" 
        :key="record.id" 
        class="bg-white rounded-xl p-4 shadow-sm border border-rose-100 hover:shadow-md transition cursor-pointer" 
        @click="viewRecord(record.id)"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center" :class="getCategoryColor(record.category)">
            <span class="text-white text-xl">{{ getCategoryIcon(record.category) }}</span>
          </div>
          <span class="text-xs text-gray-400">{{ formatDate(record.exam_date || record.date) }}</span>
        </div>
        <h3 class="font-semibold text-gray-800">{{ record.title || record.exam_type_display || 'Examen' }}</h3>
        <p class="text-sm text-gray-500 line-clamp-2">{{ record.description || record.result_summary || 'Aucune description' }}</p>
        <div class="flex items-center justify-between mt-3 pt-3 border-t border-rose-50">
          <span class="text-xs text-gray-400">Dr. {{ record.doctor || 'Médecin' }}</span>
          <span class="text-xs px-2 py-0.5 rounded-full" :class="record.is_abnormal !== undefined ? (record.is_abnormal ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700') : 'bg-yellow-100 text-yellow-700'">
            {{ record.is_abnormal !== undefined ? (record.is_abnormal ? ' Anormal' : ' Normal') : ' En attente' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Aucun résultat -->
    <div v-else-if="!loading && filteredRecords.length === 0 && records.length > 0" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <FileText class="w-16 h-16 text-rose-300 mx-auto mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucun résultat</h3>
      <p class="text-gray-500">Aucun dossier ne correspond à votre recherche</p>
    </div>

    <!-- Aucun document -->
    <div v-else-if="!loading && records.length === 0" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <FileText class="w-16 h-16 text-rose-300 mx-auto mb-4" />
      <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucun document</h3>
      <p class="text-gray-500">Aucun dossier médical trouvé</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { FileText, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'MedicalRecordsView',
  components: { FileText, Loader2 },
  setup() {
    const router = useRouter();
    const searchQuery = ref('');
    const selectedCategory = ref('');
    const records = ref([]);
    const loading = ref(true);
    const error = ref('');

    const filteredRecords = computed(() => {
      let result = records.value;
      if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(r => 
          (r.title || '').toLowerCase().includes(q) || 
          (r.description || '').toLowerCase().includes(q) ||
          (r.result_summary || '').toLowerCase().includes(q)
        );
      }
      if (selectedCategory.value) {
        result = result.filter(r => r.category === selectedCategory.value);
      }
      return result;
    });

    const getCategoryColor = (category) => {
      const colors = { 
        'Analyse': 'bg-blue-500', 
        'Échographie': 'bg-purple-500', 
        'Ordonnance': 'bg-green-500', 
        'Autre': 'bg-gray-500' 
      };
      return colors[category] || 'bg-gray-500';
    };

    const getCategoryIcon = (category) => {
      const icons = { 
        'Analyse': '', 
        'Échographie': '', 
        'Ordonnance': '', 
        'Autre': '' 
      };
      return icons[category] || '';
    };

    const viewRecord = (id) => {
      router.push(`/app/patient/records/${id}`);
    };

    const loadRecords = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        console.log(' Chargement des examens...');
        
        // ✅ Utiliser l'API des examens
        const response = await api.get('/patient/exams');
        console.log(' Examens reçus:', response.data);
        
        if (response.data && response.data.data) {
          // Transformer les examens en dossiers médicaux
          records.value = response.data.data.map(exam => ({
            id: exam.id,
            title: exam.exam_type_display || exam.exam_type || 'Examen médical',
            description: exam.result_summary || 'Résultats en attente',
            category: exam.exam_type || 'Autre',
            date: exam.exam_date || exam.created_at,
            doctor: exam.doctor_name || 'Médecin',
            status: exam.is_abnormal !== undefined ? (exam.is_abnormal ? 'abnormal' : 'completed') : 'pending',
            is_abnormal: exam.is_abnormal,
            result_summary: exam.result_summary,
            details: exam.details
          }));
        }
        
      } catch (err) {
        console.error(' Erreur chargement dossiers:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement des dossiers';
        
        // Données de fallback
        records.value = [
          {
            id: 1,
            title: 'Analyse sanguine - Premier bilan',
            description: 'Bilan sanguin complet pour le suivi de la grossesse.',
            category: 'Analyse',
            date: '2025-01-15',
            doctor: 'Dr. Martin',
            status: 'completed',
            is_abnormal: false,
            result_summary: 'Tous les résultats sont normaux.'
          },
          {
            id: 2,
            title: 'Échographie T1 - 12 semaines',
            description: 'Échographie du premier trimestre.',
            category: 'Échographie',
            date: '2025-01-10',
            doctor: 'Dr. Diallo',
            status: 'completed',
            is_abnormal: false,
            result_summary: 'Fœtus en bonne santé.'
          }
        ];
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadRecords();
    });

    return {
      records,
      filteredRecords,
      searchQuery,
      selectedCategory,
      loading,
      error,
      formatDate,
      getCategoryColor,
      getCategoryIcon,
      viewRecord
    };
  }
};
</script>