<!-- src/views/patient/MessagesView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Mes messages</h1>
      <p class="text-gray-500 text-sm">Communications avec votre médecin</p>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-rose-100 overflow-hidden flex flex-col h-[500px]">
      <!-- Chargement -->
      <div v-if="loading" class="flex-1 p-12 text-center">
        <Loader2 class="w-12 h-12 text-rose-300 animate-spin mx-auto" />
        <p class="text-gray-500 mt-4">Chargement des messages...</p>
      </div>

      <!-- Messages -->
      <div v-else ref="messagesContainer" class="flex-1 p-4 overflow-y-auto space-y-3 bg-rose-50/30">
        <div v-if="messages.length === 0" class="text-center py-12 text-gray-500">
          <MessageCircle class="w-12 h-12 text-rose-300 mx-auto mb-2" />
          <p>Aucun message</p>
          <p class="text-sm">Envoyez un message à votre médecin</p>
        </div>
        
        <div 
          v-for="msg in messages" 
          :key="msg.id" 
          class="flex"
          :class="msg.sender === 'me' ? 'justify-end' : 'justify-start'"
        >
          <div 
            class="max-w-[75%] p-3 rounded-lg"
            :class="msg.sender === 'me' ? 'bg-rose-500 text-white rounded-br-none' : 'bg-white text-gray-800 border border-rose-200 rounded-bl-none'"
          >
            <p class="text-sm">{{ msg.content }}</p>
            <p class="text-xs mt-1" :class="msg.sender === 'me' ? 'text-rose-100' : 'text-gray-400'">
              {{ formatTime(msg.created_at) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Envoi message -->
      <div class="p-3 border-t border-rose-100 bg-white">
        <div class="flex gap-2">
          <input 
            v-model="newMessage" 
            @keyup.enter="sendMessage"
            type="text" 
            placeholder="Écrire un message à votre médecin..." 
            class="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 text-sm"
          />
          <button 
            @click="sendMessage" 
            class="bg-rose-500 text-white px-4 py-2 rounded-lg hover:bg-rose-600 transition disabled:opacity-50"
            :disabled="!newMessage.trim() || sending"
          >
            <Loader2 v-if="sending" class="w-4 h-4 animate-spin" />
            <Send v-else class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue';
import { MessageCircle, Send, Loader2 } from 'lucide-vue-next';
import { formatDate } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'PatientMessagesView',
  components: { MessageCircle, Send, Loader2 },
  setup() {
    const loading = ref(true);
    const sending = ref(false);
    const newMessage = ref('');
    const messages = ref([]);
    const messagesContainer = ref(null);

    const formatTime = (date) => {
      if (!date) return '';
      try {
        const d = new Date(date);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '';
      }
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim()) return;
      
      sending.value = true;
      const content = newMessage.value.trim();
      
      try {
        // Récupérer l'ID du médecin (à adapter selon votre logique)
        // Pour l'instant, on envoie à un médecin par défaut
        const doctorId = 2; // À remplacer par l'ID du médecin de la patiente
        
        const response = await api.post('/patient/messages', {
          recipient_id: doctorId,
          content: content
        });
        
        console.log(' Message envoyé:', response.data);
        
        messages.value.push({
          id: Date.now(),
          sender: 'me',
          content: content,
          created_at: new Date().toISOString()
        });
        
        newMessage.value = '';
        
        await nextTick();
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      } catch (error) {
        console.error(' Erreur envoi message:', error);
        alert(' Erreur lors de l\'envoi du message');
      } finally {
        sending.value = false;
      }
    };

    const loadMessages = async () => {
      loading.value = true;
      try {
        const response = await api.get('/patient/messages');
        console.log(' Messages:', response.data);
        
        if (response.data && response.data.data) {
          messages.value = response.data.data;
        }
        
        await nextTick();
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      } catch (error) {
        console.error(' Erreur chargement messages:', error);
        messages.value = [];
      } finally {
        loading.value = false;
      }
    };

    watch(messages, async () => {
      await nextTick();
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
      }
    });

    onMounted(() => {
      loadMessages();
    });

    return {
      loading,
      sending,
      newMessage,
      messages,
      messagesContainer,
      formatDate,
      formatTime,
      sendMessage
    };
  }
};
</script>