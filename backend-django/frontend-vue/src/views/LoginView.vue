<!-- src/views/LoginView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 to-white flex">
    <!-- Colonne gauche - Formulaire -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12">
      <div class="w-full max-w-md">
        <!-- Bouton retour -->
        <button 
          @click="$router.push('/')" 
          class="mb-6 text-rose-500 hover:text-rose-700 transition flex items-center gap-2 text-sm font-medium"
        >
          <ArrowLeft class="w-4 h-4" /> Retour à l'accueil
        </button>

        <div class="text-center mb-8">
          <div class="inline-flex items-center gap-2">
            <Heart class="w-10 h-10 text-rose-500" />
            <span class="text-2xl font-bold text-rose-700">Suivi Grossesse</span>
          </div>
          <h1 class="text-2xl font-bold text-gray-800 mt-4">Connexion</h1>
          <p class="text-gray-500 text-sm">Connectez-vous à votre compte</p>
        </div>

        <div class="bg-white rounded-2xl shadow-xl p-6 border border-rose-50">
          <!-- Identifiants de test -->
          <div class="bg-rose-50 border border-rose-200 rounded-lg p-3 mb-4">
            <p class="text-xs text-gray-600 font-medium mb-1"> Identifiants de test :</p>
            <div class="grid grid-cols-3 gap-1 text-xs">
              <button 
                @click="fillCredentials('patient@test.com', 'password123')" 
                class="p-1.5 bg-white rounded hover:bg-rose-100 transition text-rose-600 border border-rose-200 text-center"
              >
                Patiente
              </button>
              <button 
                @click="fillCredentials('dr.martin@test.com', 'doctor123')" 
                class="p-1.5 bg-white rounded hover:bg-blue-100 transition text-blue-600 border border-blue-200 text-center"
              >
                Médecin
              </button>
              <button 
                @click="fillCredentials('admin@test.com', 'admin123')" 
                class="p-1.5 bg-white rounded hover:bg-purple-100 transition text-purple-600 border border-purple-200 text-center"
              >
                Admin
              </button>
            </div>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
              <div class="relative">
                <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input 
                  v-model="form.email" 
                  type="email" 
                  class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition text-sm"
                  placeholder="vous@email.com"
                  required
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Mot de passe</label>
              <div class="relative">
                <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input 
                  v-model="form.password" 
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full pl-10 pr-12 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition text-sm"
                  placeholder="••••••••"
                  required
                />
                <button 
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <EyeOff v-if="showPassword" class="w-4 h-4" />
                  <Eye v-else class="w-4 h-4" />
                </button>
              </div>
              <div class="flex justify-end mt-1">
                <router-link to="/forgot-password" class="text-xs text-rose-500 hover:underline">
                  Mot de passe oublié ?
                </router-link>
              </div>
            </div>

            <!-- Message d'erreur -->
            <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg text-xs">
               {{ errorMessage }}
            </div>

            <button 
              type="submit" 
              class="w-full bg-rose-500 text-white py-2.5 rounded-lg hover:bg-rose-600 transition font-medium flex items-center justify-center gap-2 disabled:opacity-50 text-sm"
              :disabled="loading"
            >
              <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
              {{ loading ? 'Connexion en cours...' : 'Se connecter' }}
            </button>
          </form>

          <div class="mt-4 text-center">
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

    <!-- Colonne droite - Image -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-rose-100 to-pink-200 items-center justify-center p-12 relative overflow-hidden">
      <div class="relative w-full max-w-lg">
        <!-- Badge en haut -->
        <div class="absolute -top-6 -left-6 z-10 bg-white rounded-2xl p-4 shadow-lg border border-rose-100">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-rose-100 rounded-full flex items-center justify-center">
              <Heart class="w-6 h-6 text-rose-500" />
            </div>
            <div>
              <p class="text-xs text-gray-500">Suivi de grossesse</p>
              <p class="text-sm font-bold text-rose-600"> Prenez soin de vous</p>
            </div>
          </div>
        </div>

        <!-- Badge en bas -->
        <div class="absolute -bottom-6 -right-6 z-10 bg-white rounded-2xl p-4 shadow-lg border border-rose-100">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <Baby class="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p class="text-xs text-gray-500">Nouvelle vie</p>
              <p class="text-sm font-bold text-blue-600"> Grossesse sereine</p>
            </div>
          </div>
        </div>

        <!-- Image -->
        <img 
          src="https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=1000&fit=crop&crop=center"
          alt="Femme enceinte"
          class="rounded-3xl w-full h-auto object-cover shadow-2xl"
        />

        <!-- Overlay décoratif -->
        <div class="absolute inset-0 rounded-3xl bg-gradient-to-t from-rose-500/10 to-transparent pointer-events-none"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Heart, Mail, Lock, Eye, EyeOff, Loader2, ArrowLeft, Baby } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'LoginView',
  components: { Heart, Mail, Lock, Eye, EyeOff, Loader2, ArrowLeft, Baby },
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

    const fillCredentials = (email, password) => {
      form.value.email = email;
      form.value.password = password;
      errorMessage.value = '';
    };

    const handleLogin = async () => {
      loading.value = true;
      errorMessage.value = '';

      try {
        console.log(' Tentative de connexion avec:', form.value.email);

        const response = await api.post('/auth/login', {
          email: form.value.email,
          password: form.value.password
        });

        console.log(' Réponse login:', response.data);

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

        console.log(' Redirection vers:', redirectPath);
        await router.push(redirectPath);

      } catch (error) {
        console.error(' Erreur login:', error);
        
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