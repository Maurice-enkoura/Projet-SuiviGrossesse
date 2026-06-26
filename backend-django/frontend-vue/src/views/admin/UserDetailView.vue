<!-- src/views/admin/UserDetailView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div class="flex items-center gap-3">
      <button @click="$router.back()" class="p-2 rounded-lg hover:bg-purple-50 transition">
        <ArrowLeft class="w-5 h-5 text-gray-600" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-800"> Détail de l'utilisateur</h1>
        <p class="text-gray-500 text-sm">{{ user?.username || 'Chargement...' }}</p>
      </div>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="bg-white rounded-xl p-12 text-center shadow-sm border border-purple-100">
      <Loader2 class="w-12 h-12 text-purple-300 animate-spin mx-auto" />
      <p class="text-gray-500 mt-4">Chargement des informations...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
       {{ error }}
    </div>

    <!-- Détails -->
    <div v-else-if="user" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Informations générales -->
      <div class="lg:col-span-1 space-y-4">
        <div class="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-16 h-16 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
              {{ getInitials(user.username) }}
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ user.username }}</h3>
              <p class="text-sm text-gray-500">{{ user.email }}</p>
              <span class="inline-block mt-1 px-2 py-0.5 rounded-full text-xs font-medium" :class="user.role === 'ADMIN' ? 'bg-purple-100 text-purple-700' : user.role === 'SOIGNANT' ? 'bg-blue-100 text-blue-700' : 'bg-rose-100 text-rose-700'">
                {{ user.role }}
              </span>
            </div>
          </div>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-500">Statut du compte</span>
              <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="getStatusClass(user.account_status)">
                {{ getStatusLabel(user.account_status) }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Téléphone</span>
              <span>{{ user.phone || 'Non renseigné' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Date de naissance</span>
              <span>{{ user.date_of_birth ? formatDate(user.date_of_birth) : 'Non renseignée' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Inscrit le</span>
              <span>{{ formatDate(user.created_at) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Dernière modification</span>
              <span>{{ formatDate(user.updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Actions</h3>
          <div class="space-y-2">
            <button v-if="user.role === 'SOIGNANT' && user.account_status === 'PENDING'" 
                    @click="validateUser" 
                    class="w-full bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition text-sm flex items-center justify-center gap-2">
              <CheckCircle class="w-4 h-4" /> Valider le compte
            </button>
            <button v-if="user.role === 'SOIGNANT' && user.account_status === 'PENDING'" 
                    @click="rejectUser" 
                    class="w-full bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition text-sm flex items-center justify-center gap-2">
              <XCircle class="w-4 h-4" /> Rejeter le compte
            </button>
            <button v-if="user.account_status === 'ACTIVE'" 
                    @click="toggleStatus" 
                    class="w-full bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition text-sm flex items-center justify-center gap-2">
              <ToggleLeft class="w-4 h-4" /> Suspendre le compte
            </button>
            <button v-if="user.account_status === 'SUSPENDED'" 
                    @click="toggleStatus" 
                    class="w-full bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition text-sm flex items-center justify-center gap-2">
              <ToggleRight class="w-4 h-4" /> Réactiver le compte
            </button>
            <button @click="deleteUser" 
                    class="w-full bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition text-sm flex items-center justify-center gap-2">
              <Trash2 class="w-4 h-4" /> Supprimer définitivement
            </button>
          </div>
        </div>
      </div>

      <!-- Informations détaillées -->
      <div class="lg:col-span-2 space-y-4">
        <!-- Si c'est un médecin -->
        <div v-if="user.role === 'SOIGNANT'" class="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Informations professionnelles</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Spécialité</span>
              <span class="font-medium">{{ user.speciality || 'Non renseignée' }}</span>
            </div>
            <div class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Numéro d'ordre</span>
              <span class="font-medium">{{ user.license_number || 'Non renseigné' }}</span>
            </div>
            <div class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Années d'expérience</span>
              <span class="font-medium">{{ user.years_of_experience || 'Non renseigné' }}</span>
            </div>
            <div class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Établissement</span>
              <span class="font-medium">{{ user.hospital_affiliation || 'Non renseigné' }}</span>
            </div>
            <div class="flex justify-between py-2">
              <span class="text-gray-500">Validé par</span>
              <span class="font-medium">{{ user.validated_by?.username || 'En attente' }}</span>
            </div>
            <div v-if="user.rejection_reason" class="flex justify-between py-2">
              <span class="text-gray-500">Motif du rejet</span>
              <span class="font-medium text-red-600">{{ user.rejection_reason }}</span>
            </div>
          </div>
        </div>

        <!-- Si c'est une patiente -->
        <div v-if="user.role === 'PATIENTE'" class="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Informations de grossesse</h3>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Enceinte</span>
              <span class="font-medium">{{ user.is_pregnant ? ' Oui' : ' Non' }}</span>
            </div>
            <div v-if="user.pregnancy_confirmation_date" class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Date de confirmation</span>
              <span class="font-medium">{{ formatDate(user.pregnancy_confirmation_date) }}</span>
            </div>
            <div v-if="user.expected_delivery_date" class="flex justify-between border-b border-purple-50 py-2">
              <span class="text-gray-500">Date prévue d'accouchement</span>
              <span class="font-medium">{{ formatDate(user.expected_delivery_date) }}</span>
            </div>
            <div v-if="user.gynecologist_name" class="flex justify-between py-2">
              <span class="text-gray-500">Gynécologue</span>
              <span class="font-medium">{{ user.gynecologist_name }}</span>
            </div>
          </div>
        </div>

        <!-- Grossesses -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Grossesses</h3>
          <div v-if="pregnancies.length > 0" class="space-y-2">
            <div v-for="preg in pregnancies" :key="preg.id" class="flex items-center justify-between p-2 hover:bg-purple-50 rounded-lg">
              <div>
                <span class="font-medium">#{{ preg.id }}</span>
                <span class="text-sm text-gray-500 ml-2">Début: {{ formatDate(preg.start_date) }}</span>
              </div>
              <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="preg.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'">
                {{ preg.is_active ? ' Active' : 'Terminée' }}
              </span>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500 text-sm">Aucune grossesse enregistrée</div>
        </div>

        <!-- Rendez-vous -->
        <div class="bg-white rounded-xl p-5 shadow-sm border border-purple-100">
          <h3 class="font-semibold text-gray-800 mb-3"> Rendez-vous</h3>
          <div v-if="appointments.length > 0" class="space-y-2">
            <div v-for="appt in appointments" :key="appt.id" class="flex items-center justify-between p-2 hover:bg-purple-50 rounded-lg">
              <div>
                <span class="font-medium">{{ formatDate(appt.date_time) }}</span>
                <span class="text-sm text-gray-500 ml-2">{{ formatTime(appt.date_time) }}</span>
                <p class="text-xs text-gray-400">{{ appt.reason }}</p>
              </div>
              <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="appt.status === 'COMPLETED' ? 'bg-green-100 text-green-700' : appt.status === 'CANCELLED' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'">
                {{ getAppointmentStatusLabel(appt.status) }}
              </span>
            </div>
          </div>
          <div v-else class="text-center py-4 text-gray-500 text-sm">Aucun rendez-vous</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  ArrowLeft, Loader2, CheckCircle, XCircle, ToggleLeft, ToggleRight, Trash2 
} from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'UserDetailView',
  components: { 
    ArrowLeft, Loader2, CheckCircle, XCircle, ToggleLeft, ToggleRight, Trash2 
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const user = ref(null);
    const pregnancies = ref([]);
    const appointments = ref([]);
    const loading = ref(true);
    const error = ref('');

    const formatTime = (dateTime) => {
      if (!dateTime) return '-';
      try {
        const d = new Date(dateTime);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '-';
      }
    };

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
        'ACTIVE': 'Actif',
        'PENDING': ' En attente',
        'REJECTED': ' Rejeté',
        'SUSPENDED': ' Suspendu'
      };
      return labels[status] || status;
    };

    const getAppointmentStatusLabel = (status) => {
      const labels = {
        'SCHEDULED': 'Programmé',
        'CONFIRMED': 'Confirmé',
        'COMPLETED': 'Effectué',
        'CANCELLED': 'Annulé'
      };
      return labels[status] || status;
    };

    const loadUser = async () => {
      const id = route.params.id;
      if (!id) {
        error.value = 'ID utilisateur manquant';
        loading.value = false;
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        // Récupérer les informations de l'utilisateur
        const userRes = await api.get(`/admin/users/${id}`);
        console.log('📥 Utilisateur:', userRes.data);
        
        if (userRes.data && userRes.data.data) {
          user.value = userRes.data.data;
        }

        // Récupérer les grossesses (si patiente)
        if (user.value?.role === 'PATIENTE') {
          try {
            const pregRes = await api.get(`/patient/pregnancies`);
            if (pregRes.data && pregRes.data.data) {
              pregnancies.value = pregRes.data.data.filter(p => p.patient === parseInt(id));
            }
          } catch (e) {
            console.log(' Aucune grossesse trouvée');
          }
        }

        // Récupérer les rendez-vous
        try {
          const apptRes = await api.get(`/patient/appointments`);
          if (apptRes.data && apptRes.data.data) {
            appointments.value = apptRes.data.data.filter(a => a.patient === parseInt(id));
          }
        } catch (e) {
          console.log(' Aucun rendez-vous trouvé');
        }

      } catch (err) {
        console.error(' Erreur chargement utilisateur:', err);
        error.value = err.response?.data?.message || 'Erreur lors du chargement';
      } finally {
        loading.value = false;
      }
    };

    const validateUser = async () => {
      if (!confirm('Valider ce compte médecin ?')) return;
      try {
        await api.post(`/admin/users/${user.value.id}/validate`);
        user.value.account_status = 'ACTIVE';
        alert(' Compte validé avec succès !');
      } catch (err) {
        console.error(' Erreur validation:', err);
        alert(' Erreur lors de la validation');
      }
    };

    const rejectUser = async () => {
      const reason = prompt('Motif du rejet :');
      if (reason === null) return;
      try {
        await api.post(`/admin/users/${user.value.id}/reject`, { reason });
        user.value.account_status = 'REJECTED';
        user.value.rejection_reason = reason;
        alert(' Compte rejeté');
      } catch (err) {
        console.error(' Erreur rejet:', err);
        alert(' Erreur lors du rejet');
      }
    };

    const toggleStatus = async () => {
      const newStatus = user.value.account_status === 'ACTIVE' ? 'SUSPENDED' : 'ACTIVE';
      const action = newStatus === 'ACTIVE' ? 'réactiver' : 'suspendre';
      
      if (!confirm(`${action.charAt(0).toUpperCase() + action.slice(1)} ce compte ?`)) return;
      
      try {
        await api.put(`/admin/users/${user.value.id}/status`, { status: newStatus });
        user.value.account_status = newStatus;
        alert(` Compte ${action} avec succès`);
      } catch (err) {
        console.error(' Erreur:', err);
        alert(` Erreur lors de la ${action}`);
      }
    };

    const deleteUser = async () => {
      if (!confirm(' Supprimer définitivement cet utilisateur ? Cette action est irréversible.')) return;
      try {
        await api.delete(`/admin/users/${user.value.id}`);
        alert(' Utilisateur supprimé');
        router.push('/app/admin/users');
      } catch (err) {
        console.error(' Erreur suppression:', err);
        alert(' Erreur lors de la suppression');
      }
    };

    onMounted(() => {
      loadUser();
    });

    return {
      user,
      pregnancies,
      appointments,
      loading,
      error,
      formatDate,
      formatTime,
      getInitials,
      getStatusClass,
      getStatusLabel,
      getAppointmentStatusLabel,
      validateUser,
      rejectUser,
      toggleStatus,
      deleteUser
    };
  }
};
</script>