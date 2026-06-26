<!-- src/components/common/Card.vue -->
<template>
  <div class="bg-white rounded-xl shadow-sm border border-rose-100 hover:shadow-md transition-all duration-300" :class="padding ? 'p-4 sm:p-6' : ''">
    <div v-if="$slots.header" class="border-b border-rose-50 pb-3 mb-4">
      <slot name="header" />
    </div>
    <div class="flex-1">
      <slot />
    </div>
    <div v-if="$slots.footer" class="border-t border-rose-50 pt-3 mt-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    padding: {
      type: Boolean,
      default: true
    }
  }
};
</script>