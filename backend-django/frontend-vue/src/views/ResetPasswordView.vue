<!-- src/views/ResetPasswordView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 to-white flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2">
          <Heart class="w-10 h-10 text-rose-500" />
          <span class="text-2xl font-bold text-rose-700">Suivi Grossesse</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mt-4">Nouveau mot de passe</h1>
        <p class="text-gray-500 text-sm">Créez un nouveau mot de passe</p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-rose-50">
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Nouveau mot de passe</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                v-model="form.password" 
                :type="showPassword ? 'text' : 'password'"
                class="w-full pl-10 pr-12 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="••••••••"
                required
                minlength="8"
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
            <p class="text-xs text-gray-400 mt-1">Minimum 8 caractères</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Confirmer le mot de passe</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                v-model="form.password_confirmation" 
                type="password"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="••••••••"
                required
              />
            </div>
          </div>
          <button 
            type="submit" 
            class="w-full bg-rose-500 text-white py-3 rounded-lg hover:bg-rose-600 transition font-medium flex items-center justify-center gap-2"
            :disabled="loading"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            {{ loading ? 'Réinitialisation...' : 'Réinitialiser le mot de passe' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <router-link to="/login" class="text-rose-500 text-sm hover:underline">
            <ArrowLeft class="w-4 h-4 inline mr-1" /> Retour à la connexion
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Heart, Lock, Eye, EyeOff, Loader2, ArrowLeft } from 'lucide-vue-next';

export default {
  name: 'ResetPasswordView',
  components: { Heart, Lock, Eye, EyeOff, Loader2, ArrowLeft },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const showPassword = ref(false);

    const form = ref({
      password: '',
      password_confirmation: ''
    });

    const handleSubmit = async () => {
      if (form.value.password !== form.value.password_confirmation) {
        alert('❌ Les mots de passe ne correspondent pas');
        return;
      }
      loading.value = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 800));
        alert('✅ Mot de passe réinitialisé avec succès !');
        router.push('/login');
      } catch (error) {
        alert('❌ Erreur lors de la réinitialisation');
      } finally {
        loading.value = false;
      }
    };

    return { form, loading, showPassword, handleSubmit };
  }
};
</script>