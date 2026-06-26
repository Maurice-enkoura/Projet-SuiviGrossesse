<!-- src/views/NotFoundView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 to-white flex items-center justify-center p-4">
    <div class="text-center max-w-lg">
      <div class="relative">
        <div class="text-9xl font-bold text-rose-200">404</div>
        <div class="absolute inset-0 flex items-center justify-center">
          <Heart class="w-32 h-32 text-rose-400 opacity-30" />
        </div>
      </div>
      
      <h1 class="text-3xl font-bold text-gray-800 mt-4">Page non trouvée</h1>
      <p class="text-gray-500 mt-2">
        Oups ! La page que vous recherchez n'existe pas ou a été déplacée.
      </p>
      
      <div class="flex flex-col sm:flex-row gap-4 justify-center mt-8">
        <router-link 
          to="/" 
          class="bg-rose-500 text-white px-6 py-3 rounded-lg hover:bg-rose-600 transition flex items-center justify-center gap-2"
        >
          <Home class="w-5 h-5" /> Accueil
        </router-link>
        <button 
          @click="goBack" 
          class="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-50 transition flex items-center justify-center gap-2"
        >
          <ArrowLeft class="w-5 h-5" /> Retour
        </button>
      </div>
      
      <div class="mt-6 text-sm text-gray-400">
        <p>Vous pouvez aussi consulter :</p>
        <div class="flex flex-wrap justify-center gap-4 mt-2">
          <router-link to="/login" class="text-rose-500 hover:underline">Connexion</router-link>
          <router-link to="/register" class="text-rose-500 hover:underline">Inscription</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Heart, Home, ArrowLeft } from 'lucide-vue-next';

export default {
  name: 'NotFoundView',
  components: { Heart, Home, ArrowLeft },
  methods: {
    goBack() {
      window.history.back();
    }
  }
};
</script>