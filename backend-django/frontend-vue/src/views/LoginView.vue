<!-- src/views/LoginView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 to-white flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2">
          <Heart class="w-10 h-10 text-rose-500" />
          <span class="text-2xl font-bold text-rose-700">Suivi Grossesse</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mt-4">Connexion</h1>
        <p class="text-gray-500 text-sm">Connectez-vous à votre compte</p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-rose-50">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                v-model="form.email" 
                type="email" 
                class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="vous@email.com"
                required
              />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Mot de passe</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'"
                class="w-full pl-10 pr-12 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="••••••••"
                required
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <EyeOff v-if="showPassword" class="w-5 h-5" />
                <Eye v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="w-4 h-4 text-rose-500 rounded border-gray-300 focus:ring-rose-400" />
              <span class="text-gray-600">Se souvenir de moi</span>
            </label>
            <router-link to="/forgot-password" class="text-rose-500 hover:underline font-medium">
              Mot de passe oublié ?
            </router-link>
          </div>
          
          <!-- Message d'erreur -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg text-sm">
            {{ errorMessage }}
          </div>

          <button 
            type="submit" 
            class="w-full bg-rose-500 text-white py-3 rounded-lg hover:bg-rose-600 transition font-medium flex items-center justify-center gap-2"
            :disabled="loading"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <!-- Identifiants de test -->
        <div class="mt-4 p-3 bg-rose-50 rounded-lg">
          <p class="text-xs text-gray-600 font-medium mb-1">🔑 Identifiants de test :</p>
          <div class="grid grid-cols-3 gap-1 text-xs">
            <button @click="fillCredentials('patient@test.com', 'password123')" class="p-1 bg-white rounded hover:bg-rose-100 transition text-rose-600">Patient</button>
            <button @click="fillCredentials('dr.martin@test.com', 'doctor123')" class="p-1 bg-white rounded hover:bg-blue-100 transition text-blue-600">Médecin</button>
            <button @click="fillCredentials('admin@test.com', 'admin123')" class="p-1 bg-white rounded hover:bg-purple-100 transition text-purple-600">Admin</button>
          </div>
        </div>

        <div class="mt-6 text-center">
          <p class="text-gray-600 text-sm">
            Pas encore de compte ? 
            <router-link to="/register" class="text-rose-500 font-semibold hover:underline">
              Créer un compte
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';
import { Heart, Mail, Lock, Eye, EyeOff, Loader2 } from 'lucide-vue-next';

export default {
  name: 'LoginView',
  components: { Heart, Mail, Lock, Eye, EyeOff, Loader2 },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const loading = ref(false);
    const showPassword = ref(false);
    const errorMessage = ref('');

    const form = ref({
      email: '',
      password: ''
    });

    // Remplir automatiquement les identifiants de test
    const fillCredentials = (email, password) => {
      form.value.email = email;
      form.value.password = password;
      errorMessage.value = '';
    };

    const handleLogin = async () => {
      loading.value = true;
      errorMessage.value = '';

      try {
        console.log('🔐 Tentative de connexion avec:', form.value.email);

        const response = await api.post('/auth/login', {
          email: form.value.email,
          password: form.value.password
        });

        console.log('✅ Réponse login:', response.data);

        const { token, user } = response.data;

        if (!token || !user) {
          throw new Error('Données de connexion incomplètes');
        }

        // Sauvegarder dans localStorage
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('userRole', user.role);

        // Mettre à jour le store
        authStore.login(user, token);

        console.log('🔐 Après connexion - Store:', {
          user: authStore.user,
          role: authStore.userRole,
          isAuthenticated: authStore.isAuthenticated
        });

        // Redirection selon le rôle
        const role = user.role;
        let redirectPath = '/app/dashboard';
        
        if (role === 'PATIENTE') {
          redirectPath = '/app/patient/pregnancies';
        } else if (role === 'SOIGNANT') {
          redirectPath = '/app/doctor/dashboard';
        } else if (role === 'ADMIN') {
          redirectPath = '/app/admin/dashboard';
        }

        console.log('🔄 Redirection vers:', redirectPath);
        
        // Rediriger
        await router.push(redirectPath);

      } catch (error) {
        console.error('❌ Erreur login:', error);
        
        if (error.response?.status === 401) {
          errorMessage.value = 'Email ou mot de passe incorrect.';
        } else if (error.response?.data?.message) {
          errorMessage.value = error.response.data.message;
        } else if (error.message) {
          errorMessage.value = error.message;
        } else {
          errorMessage.value = 'Erreur de connexion. Veuillez réessayer.';
        }
      } finally {
        loading.value = false;
      }
    };

    return { 
      form, 
      loading, 
      showPassword, 
      errorMessage,
      handleLogin,
      fillCredentials
    };
  }
};
</script>