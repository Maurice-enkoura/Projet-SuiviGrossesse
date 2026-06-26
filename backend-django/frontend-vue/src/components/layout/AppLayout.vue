<!-- src/components/layout/AppLayout.vue -->
<template>
  <div class="min-h-screen bg-rose-50">
    <main class="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'AppLayout'
};
</script>