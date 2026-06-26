<!-- src/components/common/Button.vue -->
<template>
  <button 
    :type="type"
    :disabled="loading || disabled"
    class="inline-flex items-center justify-center gap-2 px-6 py-2.5 rounded-lg font-medium transition-all duration-300"
    :class="[
      variant === 'primary' ? 'bg-rose-500 text-white hover:bg-rose-600' :
      variant === 'secondary' ? 'bg-rose-100 text-rose-700 hover:bg-rose-200' :
      variant === 'outline' ? 'border-2 border-rose-500 text-rose-500 hover:bg-rose-50' :
      variant === 'ghost' ? 'text-gray-600 hover:bg-rose-50' :
      variant === 'danger' ? 'bg-red-500 text-white hover:bg-red-600' :
      variant === 'success' ? 'bg-green-500 text-white hover:bg-green-600' :
      'bg-rose-500 text-white hover:bg-rose-600',
      size === 'sm' ? 'text-sm px-4 py-1.5' :
      size === 'lg' ? 'text-lg px-8 py-3' :
      'text-sm px-6 py-2.5',
      fullWidth ? 'w-full' : '',
      disabled || loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
    ]"
    @click="$emit('click')"
  >
    <Loader2 v-if="loading" class="w-4 h-4 animate-spin" />
    <slot name="icon" />
    <slot />
  </button>
</template>

<script>
import { Loader2 } from 'lucide-vue-next';

export default {
  name: 'Button',
  components: { Loader2 },
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outline', 'ghost', 'danger', 'success'].includes(value)
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value)
    },
    fullWidth: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click']
};
</script>