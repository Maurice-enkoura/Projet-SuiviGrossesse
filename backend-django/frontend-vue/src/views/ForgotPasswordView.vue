<!-- src/views/ForgotPasswordView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 to-white flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2">
          <Heart class="w-10 h-10 text-rose-500" />
          <span class="text-2xl font-bold text-rose-700">Suivi Grossesse</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mt-4">Mot de passe oublié</h1>
        <p class="text-gray-500 text-sm">Entrez votre email pour recevoir un lien de réinitialisation</p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-rose-50">
        <div v-if="success" class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
          <CheckCircle class="w-5 h-5 inline mr-2" />
          Un email de réinitialisation a été envoyé à votre adresse.
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input 
                v-model="email" 
                type="email" 
                class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="vous@email.com"
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
            {{ loading ? 'Envoi...' : 'Envoyer le lien' }}
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
import { Heart, Mail, CheckCircle, Loader2, ArrowLeft } from 'lucide-vue-next';

export default {
  name: 'ForgotPasswordView',
  components: { Heart, Mail, CheckCircle, Loader2, ArrowLeft },
  setup() {
    const email = ref('');
    const loading = ref(false);
    const success = ref(false);

    const handleSubmit = async () => {
      loading.value = true;
      try {
        await new Promise(resolve => setTimeout(resolve, 800));
        success.value = true;
      } catch (error) {
        alert('❌ Erreur lors de l\'envoi');
      } finally {
        loading.value = false;
      }
    };

    return { email, loading, success, handleSubmit };
  }
};
</script>