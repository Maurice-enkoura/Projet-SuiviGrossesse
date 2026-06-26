<!-- src/App.vue -->
<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();

    onMounted(() => {
      console.log('✅ App montée avec succès');
      
      // Vérifier si l'utilisateur est déjà connecté
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      const userRole = localStorage.getItem('userRole');
      
      if (token && user && userRole) {
        try {
          authStore.setToken(token);
          authStore.setUser(JSON.parse(user));
          console.log('✅ Session restaurée depuis localStorage');
        } catch (e) {
          console.warn('⚠️ Erreur restauration session:', e);
        }
      }
    });

    return {
      authStore
    };
  }
};
</script>

<style>
/* Styles globaux déjà dans main.css */
</style>