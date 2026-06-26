<!-- src/components/common/EmptyState.vue -->
<template>
  <div class="bg-white rounded-xl p-12 text-center shadow-sm border border-rose-100">
    <div class="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center mx-auto mb-4">
      <component :is="icon" class="w-8 h-8 text-rose-300" />
    </div>
    <h3 class="text-xl font-semibold text-gray-700 mb-2">{{ title }}</h3>
    <p class="text-gray-500">{{ description }}</p>
    <slot name="action" />
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    icon: {
      type: [Function, String],
      default: 'Plus'
    },
    title: {
      type: String,
      default: 'Aucune donnée'
    },
    description: {
      type: String,
      default: 'Commencez à ajouter des éléments'
    }
  }
};
</script>