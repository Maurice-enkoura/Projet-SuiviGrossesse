<!-- src/views/patient/MedicalRecordDetailView.vue -->
<template>
  <div class="space-y-6">
    <div class="flex items-center gap-3">
      <button @click="$router.back()" class="p-2 rounded-lg hover:bg-rose-50 transition">
        <ArrowLeft class="w-5 h-5 text-gray-600" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Détail du dossier</h1>
        <p class="text-gray-500 text-sm">{{ record?.title || 'Chargement...' }}</p>
      </div>
      <div class="ml-auto flex gap-2">
        <button @click="downloadRecord" class="bg-rose-500 text-white px-4 py-2 rounded-lg hover:bg-rose-600 transition text-sm flex items-center gap-2">
          <Download class="w-4 h-4" /> Télécharger
        </button>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
      <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement du dossier...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Détails -->
    <div v-else-if="record" class="bg-white rounded-xl shadow-sm border border-rose-100 overflow-hidden">
      <!-- En-tête du document -->
      <div class="p-6 border-b border-rose-50 bg-rose-50/30">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-bold text-gray-800">{{ record.title }}</h2>
            <p class="text-sm text-gray-500">Dr. {{ record.doctor || 'Médecin' }} • {{ formatDate(record.date) }}</p>
          </div>
          <span class="px-3 py-1 rounded-full text-xs font-medium" :class="getStatusClass(record)">
            {{ getStatusLabel(record) }}
          </span>
        </div>
      </div>

      <!-- Contenu -->
      <div class="p-6 space-y-6">
        <!-- Description / Compte-rendu -->
        <div>
          <h3 class="font-semibold text-gray-800 mb-2"> Compte-rendu</h3>
          <div class="bg-rose-50 rounded-lg p-4">
            <p class="text-gray-700 whitespace-pre-line">{{ record.description || record.result_summary || 'Aucun compte-rendu' }}</p>
          </div>
        </div>

        <!-- Résultats -->
        <div v-if="record.result_summary && record.result_summary !== record.description" class="border-t border-rose-50 pt-4">
          <h3 class="font-semibold text-gray-800 mb-2"> Résultats</h3>
          <div class="bg-blue-50 rounded-lg p-4">
            <p class="text-gray-700 whitespace-pre-line">{{ record.result_summary }}</p>
          </div>
        </div>

        <!-- Détails structurés -->
        <div v-if="record.details" class="border-t border-rose-50 pt-4">
          <h3 class="font-semibold text-gray-800 mb-2"> Détails</h3>
          <div class="bg-gray-50 rounded-lg p-4">
            <pre class="text-sm text-gray-700 whitespace-pre-line">{{ JSON.stringify(record.details, null, 2) }}</pre>
          </div>
        </div>

        <!-- Fichiers joints -->
        <div v-if="record.attachments && record.attachments.length > 0" class="border-t border-rose-50 pt-4">
          <h3 class="font-semibold text-gray-800 mb-3">📎 Fichiers joints ({{ record.attachments.length }})</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div 
              v-for="(file, index) in record.attachments" 
              :key="index" 
              class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-rose-50 transition cursor-pointer border border-gray-200 hover:border-rose-300"
              @click="downloadFile(file)"
            >
              <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="getFileIconClass(file.name)">
                <component :is="getFileIcon(file.name)" class="w-5 h-5 text-white" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-800 truncate">{{ file.name }}</p>
                <p class="text-xs text-gray-400">{{ file.size || 'Fichier' }}</p>
              </div>
              <Download class="w-4 h-4 text-rose-500 flex-shrink-0" />
            </div>
          </div>
        </div>

        <!-- Informations -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 border-t border-rose-50 pt-4">
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-sm text-gray-500">Catégorie</p>
            <p class="font-medium text-gray-800">{{ record.category || 'Non spécifiée' }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-sm text-gray-500">Date de l'examen</p>
            <p class="font-medium text-gray-800">{{ formatDate(record.date) }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-sm text-gray-500">Médecin traitant</p>
            <p class="font-medium text-gray-800">Dr. {{ record.doctor || 'Médecin' }}</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-sm text-gray-500">Statut</p>
            <p class="font-medium" :class="record.is_abnormal ? 'text-red-600' : 'text-green-600'">
              {{ record.is_abnormal !== undefined ? (record.is_abnormal ? ' Anormal' : ' Normal') : ' En attente' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="p-6 border-t border-rose-50 bg-gray-50 flex flex-wrap gap-3">
        <button @click="downloadRecord" class="bg-rose-500 text-white px-6 py-2 rounded-lg hover:bg-rose-600 transition text-sm flex items-center gap-2">
          <Download class="w-4 h-4" /> Télécharger le dossier
        </button>
        <button @click="printRecord" class="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-50 transition text-sm flex items-center gap-2">
          <Printer class="w-4 h-4" /> Imprimer
        </button>
        <button @click="$router.back()" class="text-gray-500 hover:text-gray-700 transition text-sm px-6 py-2">
          Retour
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  ArrowLeft, Download, Printer, Loader2, 
  FileText, FileImage, File, FilePdf 
} from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'MedicalRecordDetailView',
  components: { 
    ArrowLeft, Download, Printer, Loader2, 
    FileText, FileImage, File, FilePdf 
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const record = ref(null);
    const loading = ref(true);
    const error = ref('');

    const getStatusClass = (record) => {
      if (record.is_abnormal === true) return 'bg-red-100 text-red-700';
      if (record.is_abnormal === false) return 'bg-green-100 text-green-700';
      return 'bg-yellow-100 text-yellow-700';
    };

    const getStatusLabel = (record) => {
      if (record.is_abnormal === true) return ' Anormal';
      if (record.is_abnormal === false) return ' Normal';
      return ' En attente';
    };

  const getFileIcon = (fileName) => {
      if (!fileName) return 'File';
      const ext = fileName.split('.').pop()?.toLowerCase();
      if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) {
        return 'FileImage';
      }
      if (ext === 'pdf') {
        return 'FilePdf';
      }
      if (['doc', 'docx', 'txt', 'rtf'].includes(ext)) {
        return 'FileText';
      }
      return 'File';
    };

    const getFileIconClass = (fileName) => {
      if (!fileName) return 'bg-gray-500';
      const ext = fileName.split('.').pop()?.toLowerCase();
      if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) {
        return 'bg-green-500';
      }
      if (ext === 'pdf') {
        return 'bg-red-500';
      }
      if (['doc', 'docx', 'txt', 'rtf'].includes(ext)) {
        return 'bg-blue-500';
      }
      return 'bg-gray-500';
    };

    const loadRecord = async () => {
      const id = route.params.id;
      if (!id) {
        error.value = 'ID du dossier manquant';
        loading.value = false;
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        console.log(' Chargement examen ID:', id);
        
        // Récupérer tous les examens et filtrer par ID
        const response = await api.get('/patient/exams');
        console.log(' Examens reçus:', response.data);
        
        let exam = null;
        if (response.data && response.data.data) {
          exam = response.data.data.find(e => e.id === parseInt(id));
        }
        
        if (exam) {
          // Construire l'objet avec les fichiers
          record.value = {
            id: exam.id,
            title: exam.exam_type_display || exam.exam_type || 'Examen médical',
            description: exam.result_summary || 'Résultats en attente',
            category: exam.exam_type || 'Autre',
            date: exam.exam_date || exam.created_at,
            doctor: exam.doctor_name || 'Médecin',
            is_abnormal: exam.is_abnormal,
            result_summary: exam.result_summary,
            details: exam.details,
            file_url: exam.file_attachment,
            // Simuler des fichiers joints (à remplacer par les vrais fichiers de l'API)
            attachments: exam.file_attachment ? [
              { 
                name: exam.file_attachment.split('/').pop() || 'document.pdf', 
                size: '2.4 MB',
                url: exam.file_attachment
              }
            ] : [
              // Données de fallback pour démonstration
              { name: 'resultats_analyse.pdf', size: '1.2 MB' },
              { name: 'echographie_12semaines.jpg', size: '3.8 MB' }
            ]
          };
        } else {
          error.value = 'Dossier non trouvé';
        }
        
      } catch (err) {
        console.error(' Erreur chargement dossier:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    const downloadRecord = () => {
      alert(' Téléchargement du dossier complet...');
    };

    const downloadFile = (file) => {
      alert(`📥 Téléchargement de ${file.name}...`);
      if (file.url) {
        window.open(file.url, '_blank');
      }
    };

    const printRecord = () => {
      window.print();
    };

    onMounted(() => {
      loadRecord();
    });

    return {
      record,
      loading,
      error,
      formatDate,
      getStatusClass,
      getStatusLabel,
      getFileIcon,
      getFileIconClass,
      downloadRecord,
      downloadFile,
      printRecord
    };
  }
};
</script>