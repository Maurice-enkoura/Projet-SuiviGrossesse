<!-- src/views/doctor/MessagesView.vue -->
<template>
  <div class="space-y-6">
    <!-- En-tête -->
    <div>
      <h1 class="text-2xl font-bold text-gray-800"> Messages</h1>
      <p class="text-gray-500 text-sm">Communications avec vos patientes</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Liste des conversations -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-xl shadow-sm border border-blue-100 overflow-hidden">
          <div class="p-3 border-b border-blue-50">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="🔍 Rechercher une patiente..." 
              class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400 text-sm"
            />
          </div>
          <div class="divide-y divide-blue-50 max-h-[500px] overflow-y-auto">
            <div 
              v-for="conversation in filteredConversations" 
              :key="conversation.patient_id"
              @click="selectConversation(conversation)"
              class="p-3 hover:bg-blue-50 cursor-pointer transition"
              :class="selectedPatient?.patient_id === conversation.patient_id ? 'bg-blue-50' : ''"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm" 
                  :class="conversation.unread ? 'bg-blue-500' : 'bg-gray-400'">
                  {{ getInitials(conversation.patient_name) }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p class="font-medium text-gray-800 truncate">{{ conversation.patient_name }}</p>
                    <span class="text-xs text-gray-400">{{ formatTime(conversation.last_message_date) }}</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-gray-500 truncate">{{ conversation.last_message || 'Aucun message' }}</p>
                    <span v-if="conversation.unread" class="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0"></span>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="loading" class="p-8 text-center">
              <Loader2 class="w-8 h-8 text-blue-300 animate-spin mx-auto" />
              <p class="text-gray-500 text-sm mt-2">Chargement...</p>
            </div>
            <div v-if="!loading && filteredConversations.length === 0" class="p-8 text-center text-gray-500 text-sm">
              Aucune conversation
            </div>
          </div>
        </div>
      </div>

      <!-- Zone de conversation -->
      <div class="lg:col-span-2">
        <div v-if="selectedPatient" class="bg-white rounded-xl shadow-sm border border-blue-100 overflow-hidden flex flex-col h-[550px]">
          <!-- En-tête conversation -->
          <div class="p-4 border-b border-blue-50 flex items-center gap-3">
            <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm bg-blue-500">
              {{ getInitials(selectedPatient.patient_name) }}
            </div>
            <div>
              <p class="font-medium text-gray-800">{{ selectedPatient.patient_name }}</p>
              <p class="text-xs text-gray-500">Patiente #{{ selectedPatient.patient_id }}</p>
            </div>
          </div>

          <!-- Messages -->
          <div ref="messagesContainer" class="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-50">
            <div v-if="messages.length === 0" class="text-center py-12 text-gray-500">
              <MessageCircle class="w-12 h-12 text-gray-300 mx-auto mb-2" />
              <p>Aucun message</p>
              <p class="text-sm">Commencez la conversation</p>
            </div>
            
            <div 
              v-for="msg in messages" 
              :key="msg.id" 
              class="flex"
              :class="msg.sender === 'me' ? 'justify-end' : 'justify-start'"
            >
              <div 
                class="max-w-[75%] p-3 rounded-lg"
                :class="msg.sender === 'me' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'"
              >
                <p class="text-sm">{{ msg.content }}</p>
                <p class="text-xs mt-1" :class="msg.sender === 'me' ? 'text-blue-100' : 'text-gray-400'">
                  {{ formatTime(msg.created_at) }}
                </p>
              </div>
            </div>
          </div>

          <!-- Envoi message -->
          <div class="p-3 border-t border-blue-50">
            <div class="flex gap-2">
              <input 
                v-model="newMessage" 
                @keyup.enter="sendMessage"
                type="text" 
                placeholder="Écrire un message..." 
                class="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-400 text-sm"
              />
              <button 
                @click="sendMessage" 
                class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition disabled:opacity-50"
                :disabled="!newMessage.trim() || sending"
              >
                <Loader2 v-if="sending" class="w-4 h-4 animate-spin" />
                <Send v-else class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Sélectionner une conversation -->
        <div v-else class="bg-white rounded-xl shadow-sm border border-blue-100 p-12 text-center h-[550px] flex flex-col items-center justify-center">
          <MessageCircle class="w-16 h-16 text-blue-300 mx-auto mb-4" />
          <h3 class="text-xl font-semibold text-gray-700 mb-2">Aucune conversation sélectionnée</h3>
          <p class="text-gray-500 text-sm">Sélectionnez une patiente dans la liste pour consulter vos messages</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { MessageCircle, Send, Loader2 } from 'lucide-vue-next';
import { formatDate, getInitials } from '@/utils/helpers';
import api from '@/services/api';

export default {
  name: 'DoctorMessagesView',
  components: { MessageCircle, Send, Loader2 },
  setup() {
    const searchQuery = ref('');
    const conversations = ref([]);
    const selectedPatient = ref(null);
    const messages = ref([]);
    const newMessage = ref('');
    const sending = ref(false);
    const loading = ref(true);
    const messagesContainer = ref(null);

    const filteredConversations = computed(() => {
      if (!searchQuery.value) return conversations.value;
      const q = searchQuery.value.toLowerCase();
      return conversations.value.filter(c => 
        c.patient_name.toLowerCase().includes(q)
      );
    });

    const formatTime = (date) => {
      if (!date) return '';
      try {
        const d = new Date(date);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      } catch {
        return '';
      }
    };

    const selectConversation = (conversation) => {
      selectedPatient.value = conversation;
      loadMessages(conversation.patient_id);
    };

    const loadConversations = async () => {
      loading.value = true;
      try {
        const response = await api.get('/caregiver/messages');
        console.log(' Messages:', response.data);
        
        if (response.data && response.data.data) {
          conversations.value = response.data.data;
        }
      } catch (error) {
        console.error(' Erreur chargement conversations:', error);
        conversations.value = [];
      } finally {
        loading.value = false;
      }
    };

    const loadMessages = async (patientId) => {
      try {
        const response = await api.get(`/caregiver/messages/${patientId}`);
        console.log(' Messages:', response.data);
        
        if (response.data && response.data.data) {
          messages.value = response.data.data;
        }
        
        // Scroll en bas
        await nextTick();
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
      } catch (error) {
        console.error(' Erreur chargement messages:', error);
        messages.value = [];
      }
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim() || !selectedPatient.value) return;
      
      sending.value = true;
      const content = newMessage.value.trim();
      
      try {
        const response = await api.post('/caregiver/messages', {
          recipient_id: selectedPatient.value.patient_id,
          content: content
        });
        
        console.log('📥 Message envoyé:', response.data);
        
        // Ajouter le message localement
        messages.value.push({
          id: Date.now(),
          sender: 'me',
          content: content,
          created_at: new Date().toISOString()
        });
        
        newMessage.value = '';
        
        // Scroll en bas
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

    // Scroll en bas quand les messages changent
    watch(messages, async () => {
      await nextTick();
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
      }
    });

    onMounted(() => {
      loadConversations();
    });

    return {
      searchQuery,
      conversations,
      filteredConversations,
      selectedPatient,
      messages,
      newMessage,
      sending,
      loading,
      messagesContainer,
      formatDate,
      formatTime,
      getInitials,
      selectConversation,
      sendMessage
    };
  }
};
</script>