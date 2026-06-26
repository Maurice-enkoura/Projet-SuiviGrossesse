<!-- src/components/common/Modal.vue -->
<template>
  <Teleport to="body">
    <div 
      v-if="modelValue" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      @click.self="close"
    >
      <!-- Overlay -->
      <div 
        class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        @click="close"
      />
      
      <!-- Modal -->
      <div 
        class="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto animate-fade-in"
        :class="size === 'sm' ? 'max-w-sm' : size === 'lg' ? 'max-w-2xl' : 'max-w-lg'"
      >
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-rose-50">
          <h3 class="text-lg font-bold text-gray-800">
            <slot name="title" />
          </h3>
          <button 
            @click="close" 
            class="p-1.5 rounded-lg hover:bg-rose-50 transition text-gray-400 hover:text-gray-600"
          >
            <X class="w-5 h-5" />
          </button>
        </div>
        
        <!-- Body -->
        <div class="p-4">
          <slot />
        </div>
        
        <!-- Footer -->
        <div v-if="$slots.footer" class="flex justify-end gap-3 p-4 border-t border-rose-50">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
import { X } from 'lucide-vue-next';

export default {
  name: 'Modal',
  components: { X },
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value)
    }
  },
  emits: ['update:modelValue'],
  methods: {
    close() {
      this.$emit('update:modelValue', false);
    }
  }
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>