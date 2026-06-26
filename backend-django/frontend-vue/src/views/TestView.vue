<!-- src/views/TestView.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-rose-50">
    <div class="bg-white p-8 rounded-2xl shadow-xl">
      <h1 class="text-3xl font-bold text-rose-600">✅ Test réussi !</h1>
      <p class="mt-2 text-gray-600">La page fonctionne correctement.</p>
      <p class="mt-4 text-sm text-gray-400">Heure: {{ new Date().toLocaleString() }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestView',
  mounted() {
    console.log('✅ TestView monté');
  }
};
</script>