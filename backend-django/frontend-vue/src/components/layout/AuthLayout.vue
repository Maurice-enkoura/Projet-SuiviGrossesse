<!-- src/components/layout/AuthLayout.vue -->
<template>
  <div class="min-h-screen bg-rose-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-rose-100 fixed top-0 left-0 right-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <router-link to="/app/dashboard" class="flex items-center gap-2 group">
            <div class="w-10 h-10 bg-gradient-to-r from-rose-400 to-rose-600 rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300">
              <Heart class="w-5 h-5 text-white" />
            </div>
            <div>
              <span class="text-lg font-bold text-rose-700">Suivi Grossesse</span>
              <p class="text-xs text-rose-400 -mt-0.5">Espace sécurisé</p>
            </div>
          </router-link>

          <!-- Navigation Desktop -->
          <nav class="hidden md:flex items-center gap-1">
            <router-link 
              v-for="item in navItems" 
              :key="item.path"
              :to="item.path"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
              :class="$route.path === item.path ? 'bg-rose-100 text-rose-700' : 'text-gray-600 hover:bg-rose-50 hover:text-rose-600'"
            >
              <component :is="item.icon" class="w-4 h-4 inline mr-2" />
              {{ item.label }}
            </router-link>
          </nav>

          <!-- User Menu -->
          <div class="flex items-center gap-3">
            <button @click="toggleTheme" class="p-2 rounded-lg hover:bg-rose-50 transition">
              <Sun v-if="isDark" class="w-5 h-5 text-rose-500" />
              <Moon v-else class="w-5 h-5 text-rose-500" />
            </button>
            
            <div class="relative" @click="toggleDropdown">
              <button class="flex items-center gap-2 p-2 rounded-lg hover:bg-rose-50 transition group">
                <div class="w-8 h-8 bg-gradient-to-r from-rose-400 to-rose-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                  {{ initials }}
                </div>
                <span class="hidden sm:block text-sm font-medium text-gray-700">{{ user?.name }}</span>
                <ChevronDown class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="{ 'rotate-180': isOpen }" />
              </button>
              
              <div v-if="isOpen" class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-rose-100 overflow-hidden z-50">
                <div class="p-3 border-b border-rose-50">
                  <p class="font-medium text-gray-800">{{ user?.name }}</p>
                  <p class="text-xs text-gray-500">{{ user?.email }}</p>
                  <span class="inline-block mt-1 px-2 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-700">
                    {{ userRoleLabel }}
                  </span>
                </div>
                <div class="py-1">
                  <router-link :to="profileRoute" class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-rose-50 transition">
                    <User class="w-4 h-4 text-rose-500" />
                    Mon profil
                  </router-link>
                  <router-link :to="settingsRoute" class="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-rose-50 transition">
                    <Settings class="w-4 h-4 text-rose-500" />
                    Paramètres
                  </router-link>
                  <hr class="my-1 border-rose-50" />
                  <button @click="logout" class="flex items-center gap-3 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition">
                    <LogOut class="w-4 h-4" />
                    Déconnexion
                  </button>
                </div>
              </div>
            </div>

            <!-- Menu Mobile Toggle -->
            <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="md:hidden p-2 rounded-lg hover:bg-rose-50 transition">
              <Menu class="w-6 h-6 text-rose-600" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Menu -->
    <div v-if="isMobileMenuOpen" class="md:hidden fixed inset-0 bg-black/50 z-40" @click="isMobileMenuOpen = false">
      <div class="bg-white w-72 h-full p-4 shadow-xl" @click.stop>
        <div class="flex justify-between items-center mb-4">
          <span class="font-bold text-rose-700">Menu</span>
          <button @click="isMobileMenuOpen = false" class="p-2 rounded-lg hover:bg-rose-50 transition">
            <X class="w-5 h-5 text-rose-600" />
          </button>
        </div>
        <nav class="space-y-1">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path"
            class="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === item.path ? 'bg-rose-100 text-rose-700' : 'text-gray-600 hover:bg-rose-50'"
            @click="isMobileMenuOpen = false"
          >
            <component :is="item.icon" class="w-5 h-5" />
            {{ item.label }}
          </router-link>
        </nav>
        <hr class="my-4 border-rose-100" />
        <button @click="logout" class="flex items-center gap-3 w-full px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition text-sm font-medium">
          <LogOut class="w-5 h-5" />
          Déconnexion
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main class="pt-20 pb-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <router-view />
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { 
  Heart, User, Settings, LogOut, Menu, X, 
  ChevronDown, Sun, Moon, 
  Calendar, Baby, FileText, MessageCircle, 
  Users, LayoutDashboard, Activity, Stethoscope,
  Clock  // ✅ AJOUTER Clock ici
} from 'lucide-vue-next';

export default {
  name: 'AuthLayout',
  components: {
    Heart, User, Settings, LogOut, Menu, X, 
    ChevronDown, Sun, Moon,
    Calendar, Baby, FileText, MessageCircle,
    Users, LayoutDashboard, Activity, Stethoscope,
    Clock  // ✅ AJOUTER Clock ici aussi
  },
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const isOpen = ref(false);
    const isMobileMenuOpen = ref(false);
    const isDark = ref(false);

    const user = computed(() => authStore.user);
    const userRole = computed(() => authStore.userRole);

    const initials = computed(() => {
      if (!user.value?.username && !user.value?.name) return 'U';
      const name = user.value?.username || user.value?.name || 'Utilisateur';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    });

    const userRoleLabel = computed(() => {
      const roles = {
        'PATIENTE': 'Patient(e)',
        'SOIGNANT': 'Médecin',
        'ADMIN': 'Administrateur'
      };
      return roles[userRole.value] || userRole.value;
    });

    const profileRoute = computed(() => {
      const role = userRole.value;
      if (role === 'PATIENTE') return '/app/patient/profile';
      if (role === 'SOIGNANT') return '/app/doctor/profile';
      return '/app/admin/users';
    });

    const settingsRoute = computed(() => {
      const role = userRole.value;
      if (role === 'PATIENTE') return '/app/patient/settings';
      if (role === 'SOIGNANT') return '/app/doctor/settings';
      return '/app/admin/settings';
    });

    const navItems = computed(() => {
      const role = userRole.value;
      
      if (role === 'PATIENTE') {
        return [
          { path: '/app/patient/pregnancies', label: ' Grossesses', icon: Baby },
          { path: '/app/patient/appointments', label: ' Rendez-vous', icon: Calendar },
          { path: '/app/patient/records', label: ' Dossiers', icon: FileText },
          { path: '/app/patient/messages', label: ' Messages', icon: MessageCircle },
          { path: '/app/patient/profile', label: ' Profil', icon: User },
        ];
      } else if (role === 'SOIGNANT') {
        return [
          { path: '/app/doctor/dashboard', label: ' Dashboard', icon: LayoutDashboard },
          { path: '/app/doctor/patients', label: ' Patient(e)s', icon: Users },
          { path: '/app/doctor/appointments', label: ' Rendez-vous', icon: Calendar },
          { path: '/app/doctor/consultations', label: ' Consultations', icon: Stethoscope },
          { path: '/app/doctor/messages', label: ' Messages', icon: MessageCircle },
          { path: '/app/doctor/schedule', label: ' Horaires', icon: Clock },
          { path: '/app/doctor/profile', label: ' Profil', icon: User },
        ];
      } else if (role === 'ADMIN') {
        return [
          { path: '/app/admin/dashboard', label: ' Dashboard', icon: LayoutDashboard },
          { path: '/app/admin/users', label: ' Utilisateurs', icon: Users },
          { path: '/app/admin/stats', label: ' Statistiques', icon: Activity },
          { path: '/app/admin/logs', label: ' Logs', icon: FileText },
          { path: '/app/admin/settings', label: ' Paramètres', icon: Settings },
        ];
      }
      return [];
    });

    const toggleDropdown = () => {
      isOpen.value = !isOpen.value;
    };

    const toggleTheme = () => {
      isDark.value = !isDark.value;
      document.documentElement.classList.toggle('dark');
    };

    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    const handleClickOutside = (event) => {
      if (isOpen.value && !event.target.closest('.relative')) {
        isOpen.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      user,
      userRole,
      initials,
      userRoleLabel,
      profileRoute,
      settingsRoute,
      navItems,
      isOpen,
      isMobileMenuOpen,
      isDark,
      toggleDropdown,
      toggleTheme,
      logout
    };
  }
};
</script>