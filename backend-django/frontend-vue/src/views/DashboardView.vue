<!-- src/views/DashboardView.vue -->
<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white rounded-xl shadow-sm p-8 text-center">
        <div class="flex flex-col items-center gap-4">
          <div class="w-20 h-20 bg-rose-100 rounded-full flex items-center justify-center">
            <Loader2 class="w-10 h-10 text-rose-500 animate-spin" />
          </div>
          <h2 class="text-xl font-semibold text-gray-800">Redirection en cours...</h2>
          <p class="text-gray-500">Bienvenue {{ userName }}</p>
          <p class="text-sm text-gray-400">Rôle : {{ userRoleLabel }}</p>
          
          <!-- Informations de débogage -->
          <div class="text-xs text-gray-400 space-y-1">
            <p>ID: {{ userId }}</p>
            <p>Email: {{ userEmail }}</p>
            <p>Store auth: {{ authStatus }}</p>
          </div>

          <div class="flex flex-wrap gap-3 mt-4">
            <button 
              v-if="userRole === 'PATIENTE'" 
              @click="redirectTo('/app/patient/pregnancies')"
              class="bg-rose-500 text-white px-6 py-2 rounded-lg hover:bg-rose-600 transition"
            >
               Espace Patient(e)
            </button>
            <button 
              v-else-if="userRole === 'SOIGNANT'" 
              @click="redirectTo('/app/doctor/dashboard')"
              class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition"
            >
              🩺 Espace Médecin
            </button>
            <button 
              v-else-if="userRole === 'ADMIN'" 
              @click="redirectTo('/app/admin/dashboard')"
              class="bg-purple-500 text-white px-6 py-2 rounded-lg hover:bg-purple-600 transition"
            >
              ⚙️ Espace Admin
            </button>
            <button 
              v-else
              @click="logout" 
              class="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition"
            >
              Se déconnecter
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Loader2 } from 'lucide-vue-next';

export default {
  name: 'DashboardView',
  components: { Loader2 },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const redirected = ref(false);

    // Computed avec fallback
    const userName = computed(() => {
      const user = authStore.user;
      return user?.username || user?.name || 'Utilisateur';
    });

    const userEmail = computed(() => {
      const user = authStore.user;
      return user?.email || 'Non défini';
    });

    const userId = computed(() => {
      const user = authStore.user;
      return user?.id || 'Non défini';
    });

    const userRole = computed(() => {
      const role = authStore.userRole;
      console.log('📌 Dashboard - userRole:', role);
      console.log('📌 Dashboard - user complet:', authStore.user);
      return role;
    });

    const authStatus = computed(() => {
      return `Auth: ${authStore.isAuthenticated}, Token: ${!!authStore.token}`;
    });

    const userRoleLabel = computed(() => {
      const roles = {
        'PATIENTE': 'Patient(e)',
        'SOIGNANT': 'Médecin',
        'ADMIN': 'Administrateur'
      };
      return roles[userRole.value] || userRole.value || 'Non défini';
    });

    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    const redirectTo = (path) => {
      console.log('🔄 Redirection manuelle vers:', path);
      router.push(path);
    };

    const restoreFromLocalStorage = () => {
      const storedUser = localStorage.getItem('user');
      const storedRole = localStorage.getItem('userRole');
      const storedToken = localStorage.getItem('token');
      
      console.log(' Dashboard - localStorage:', { storedUser, storedRole, storedToken });
      
      if (storedUser && storedRole && storedToken) {
        try {
          const user = JSON.parse(storedUser);
          authStore.setUser(user);
          authStore.setToken(storedToken);
          console.log(' Dashboard - Restauré depuis localStorage:', user);
          return true;
        } catch (e) {
          console.error('Erreur parsing user:', e);
        }
      }
      return false;
    };

    onMounted(() => {
      if (redirected.value) return;
      redirected.value = true;

      console.log(' Dashboard - État store au montage:', {
        user: authStore.user,
        userRole: authStore.userRole,
        isAuthenticated: authStore.isAuthenticated,
        token: authStore.token
      });

      // Si le store est vide, restaurer depuis localStorage
      if (!authStore.user || !authStore.userRole) {
        const restored = restoreFromLocalStorage();
        if (!restored) {
          console.warn(' Aucune donnée trouvée, redirection vers login');
          router.push('/login');
          return;
        }
      }

      // Redirection automatique
      const role = userRole.value;
      console.log(' Dashboard - Redirection pour rôle:', role);
      
      if (role === 'PATIENTE') {
        router.push('/app/patient/pregnancies');
      } else if (role === 'SOIGNANT') {
        router.push('/app/doctor/dashboard');
      } else if (role === 'ADMIN') {
        router.push('/app/admin/dashboard');
      } else {
        console.warn(' Rôle non reconnu:', role);
        // Si le rôle n'est pas reconnu, essayer de le récupérer depuis localStorage
        const storedRole = localStorage.getItem('userRole');
        if (storedRole === 'PATIENTE') {
          router.push('/app/patient/pregnancies');
        } else if (storedRole === 'SOIGNANT') {
          router.push('/app/doctor/dashboard');
        } else if (storedRole === 'ADMIN') {
          router.push('/app/admin/dashboard');
        } else {
          router.push('/login');
        }
      }
    });

    return {
      userName,
      userEmail,
      userId,
      userRole,
      userRoleLabel,
      authStatus,
      logout,
      redirectTo
    };
  }
};
</script>