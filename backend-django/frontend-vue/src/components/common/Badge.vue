<!-- src/components/common/Badge.vue -->
<template>
  <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="[
      variant === 'rose' ? 'bg-rose-100 text-rose-700' :
      variant === 'green' ? 'bg-green-100 text-green-700' :
      variant === 'blue' ? 'bg-blue-100 text-blue-700' :
      variant === 'yellow' ? 'bg-yellow-100 text-yellow-700' :
      variant === 'red' ? 'bg-red-100 text-red-700' :
      variant === 'purple' ? 'bg-purple-100 text-purple-700' :
      variant === 'gray' ? 'bg-gray-100 text-gray-700' :
      'bg-rose-100 text-rose-700'
    ]"
  >
    <slot />
  </span>
</template>

<script>
export default {
  name: 'Badge',
  props: {
    variant: {
      type: String,
      default: 'rose',
      validator: (value) => ['rose', 'green', 'blue', 'yellow', 'red', 'purple', 'gray'].includes(value)
    }
  }
};
</script>