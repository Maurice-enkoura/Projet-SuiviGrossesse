<!-- src/views/RegisterView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 to-white flex items-center justify-center p-4">
    <div class="w-full max-w-2xl">
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2">
          <Heart class="w-10 h-10 text-rose-500" />
          <span class="text-2xl font-bold text-rose-700">Suivi Grossesse</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mt-4">Créer un compte</h1>
        <p class="text-gray-500 text-sm">Inscrivez-vous pour commencer</p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-rose-50">
        <!-- Message d'information -->
        <div class="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg text-sm mb-6">
          <p class="font-medium"> Comptes sécurisés</p>
          <p class="text-xs mt-1">
            Les comptes des médecins sont vérifiés par notre équipe.
            Les patientes doivent confirmer leur grossesse.
          </p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- Rôle -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Je suis *</label>
            <div class="grid grid-cols-3 gap-2">
              <button 
                type="button"
                @click="form.role = 'PATIENTE'"
                class="py-2 px-4 rounded-lg border text-sm font-medium transition"
                :class="form.role === 'PATIENTE' ? 'bg-rose-500 text-white border-rose-500' : 'bg-white text-gray-700 border-gray-200 hover:border-rose-300'"
              >
                 Patiente
              </button>
              <button 
                type="button"
                @click="form.role = 'SOIGNANT'"
                class="py-2 px-4 rounded-lg border text-sm font-medium transition"
                :class="form.role === 'SOIGNANT' ? 'bg-rose-500 text-white border-rose-500' : 'bg-white text-gray-700 border-gray-200 hover:border-rose-300'"
              >
                 Médecin/Sage-femme
              </button>
              <button 
                type="button"
                @click="form.role = 'ADMIN'"
                class="py-2 px-4 rounded-lg border text-sm font-medium transition"
                :class="form.role === 'ADMIN' ? 'bg-rose-500 text-white border-rose-500' : 'bg-white text-gray-700 border-gray-200 hover:border-rose-300'"
              >
                 Admin
              </button>
            </div>
          </div>

          <!-- Informations de base -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Nom d'utilisateur *</label>
              <input 
                v-model="form.username" 
                type="text" 
                class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="john_doe"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Email *</label>
              <input 
                v-model="form.email" 
                type="email" 
                class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="vous@email.com"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Mot de passe *</label>
              <div class="relative">
                <input 
                  v-model="form.password" 
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                  placeholder="••••••••"
                  required
                />
                <button 
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <EyeOff v-if="showPassword" class="w-5 h-5" />
                  <Eye v-else class="w-5 h-5" />
                </button>
              </div>
              <p class="text-xs text-gray-400 mt-1">Minimum 8 caractères</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Confirmer le mot de passe *</label>
              <input 
                v-model="form.password_confirmation" 
                type="password"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition"
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <!-- Champs pour PATIENTE -->
          <div v-if="form.role === 'PATIENTE'" class="border-t border-rose-100 pt-4">
            <h3 class="font-medium text-gray-800 mb-3"> Informations de grossesse</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Date de début de grossesse *</label>
                <input 
                  v-model="form.pregnancy_start_date" 
                  type="date" 
                  class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Date prévue d'accouchement</label>
                <input 
                  v-model="form.expected_delivery_date" 
                  type="date" 
                  class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Nom de votre gynécologue/sage-femme</label>
                <input 
                  v-model="form.gynecologist_name" 
                  type="text" 
                  class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
                  placeholder="Dr. Martin"
                />
                <p class="text-xs text-gray-400 mt-1">Facultatif - Pour que votre médecin puisse vous trouver</p>
              </div>
            </div>
            <div class="flex items-center gap-2 mt-3">
              <input type="checkbox" v-model="form.confirm_pregnancy" class="w-4 h-4 text-rose-500 rounded" required />
              <span class="text-sm text-gray-600">Je confirme que je suis enceinte et que les informations fournies sont correctes</span>
            </div>
          </div>

          <!-- Champs pour SOIGNANT -->
          <div v-if="form.role === 'SOIGNANT'" class="border-t border-rose-100 pt-4">
            <h3 class="font-medium text-gray-800 mb-3"> Informations professionnelles</h3>
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Spécialité *</label>
                  <select v-model="form.speciality" class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400" required>
                    <option value="">Sélectionner</option>
                    <option value="Gynécologie">Gynécologie</option>
                    <option value="Obstétrique">Obstétrique</option>
                    <option value="Sage-femme">Sage-femme</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Numéro d'ordre (RPPS/ADELI) *</label>
                  <input 
                    v-model="form.license_number" 
                    type="text" 
                    class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
                    placeholder="123456789"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Années d'expérience</label>
                  <input 
                    v-model="form.years_of_experience" 
                    type="number" 
                    class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
                    placeholder="5"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">Établissement</label>
                  <input 
                    v-model="form.hospital_affiliation" 
                    type="text" 
                    class="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:border-rose-400"
                    placeholder="CHU de Brazzaville"
                  />
                </div>
              </div>
              
              <!-- Documents -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5"> Documents professionnels *</label>
                <div class="space-y-3">
                  <div class="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <File class="w-5 h-5 text-blue-500" />
                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-700">Diplôme de médecine/Sage-femme</p>
                      <p class="text-xs text-gray-500">PDF, JPG, PNG - Max 5MB</p>
                    </div>
                    <input type="file" @change="handleFileUpload('diploma', $event)" class="hidden" ref="diplomaInput" accept=".pdf,.jpg,.jpeg,.png" />
                    <button type="button" @click="$refs.diplomaInput.click()" class="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 transition">
                      Choisir
                    </button>
                    <span v-if="form.diploma_file" class="text-xs text-green-600">✓ Fichier sélectionné</span>
                  </div>
                  
                  <div class="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <File class="w-5 h-5 text-blue-500" />
                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-700">Carte professionnelle</p>
                      <p class="text-xs text-gray-500">PDF, JPG, PNG - Max 5MB</p>
                    </div>
                    <input type="file" @change="handleFileUpload('license', $event)" class="hidden" ref="licenseInput" accept=".pdf,.jpg,.jpeg,.png" />
                    <button type="button" @click="$refs.licenseInput.click()" class="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 transition">
                      Choisir
                    </button>
                    <span v-if="form.license_file" class="text-xs text-green-600">✓ Fichier sélectionné</span>
                  </div>
                  
                  <div class="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <File class="w-5 h-5 text-blue-500" />
                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-700">Pièce d'identité</p>
                      <p class="text-xs text-gray-500">PDF, JPG, PNG - Max 5MB</p>
                    </div>
                    <input type="file" @change="handleFileUpload('id_card', $event)" class="hidden" ref="idCardInput" accept=".pdf,.jpg,.jpeg,.png" />
                    <button type="button" @click="$refs.idCardInput.click()" class="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 transition">
                      Choisir
                    </button>
                    <span v-if="form.id_card_file" class="text-xs text-green-600">✓ Fichier sélectionné</span>
                  </div>
                </div>
                <p class="text-xs text-amber-600 mt-2">
                   Ces documents seront vérifiés par l'administrateur avant validation de votre compte
                </p>
              </div>
            </div>
          </div>

          <!-- Message d'erreur -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
             {{ errorMessage }}
          </div>

          <button 
            type="submit" 
            class="w-full bg-rose-500 text-white py-3 rounded-lg hover:bg-rose-600 transition font-medium flex items-center justify-center gap-2 disabled:opacity-50"
            :disabled="loading || !isFormValid"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            {{ loading ? 'Inscription en cours...' : 'S\'inscrire' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-gray-600 text-sm">
            Déjà un compte ? 
            <router-link to="/login" class="text-rose-500 font-semibold hover:underline">
              Se connecter
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Heart, Eye, EyeOff, File, Loader2 } from 'lucide-vue-next';
import api from '@/services/api';

export default {
  name: 'RegisterView',
  components: { Heart, Eye, EyeOff, File, Loader2 },
  setup() {
    const router = useRouter();
    const loading = ref(false);
    const showPassword = ref(false);
    const errorMessage = ref('');

    const form = ref({
      username: '',
      email: '',
      password: '',
      password_confirmation: '',
      role: 'PATIENTE',
      // Patient
      pregnancy_start_date: '',
      expected_delivery_date: '',
      gynecologist_name: '',
      confirm_pregnancy: false,
      // Soignant
      speciality: '',
      license_number: '',
      years_of_experience: '',
      hospital_affiliation: '',
      diploma_file: null,
      license_file: null,
      id_card_file: null
    });

    const isFormValid = computed(() => {
      if (!form.value.username || !form.value.email || !form.value.password) return false;
      if (form.value.password !== form.value.password_confirmation) return false;
      
      if (form.value.role === 'PATIENTE') {
        if (!form.value.pregnancy_start_date) return false;
        if (!form.value.confirm_pregnancy) return false;
      }
      
      if (form.value.role === 'SOIGNANT') {
        if (!form.value.speciality) return false;
        if (!form.value.license_number) return false;
      }
      
      return true;
    });

    const handleFileUpload = (type, event) => {
      const file = event.target.files[0];
      if (file) {
        // Vérifier la taille (5MB max)
        if (file.size > 5 * 1024 * 1024) {
          errorMessage.value = 'Le fichier est trop volumineux (max 5MB)';
          return;
        }
        form.value[`${type}_file`] = file;
      }
    };

    const handleRegister = async () => {
      loading.value = true;
      errorMessage.value = '';

      try {
        const formData = new FormData();
        formData.append('username', form.value.username);
        formData.append('email', form.value.email);
        formData.append('password', form.value.password);
        formData.append('password_confirmation', form.value.password_confirmation);
        formData.append('role', form.value.role);

        // Données patiente
        if (form.value.role === 'PATIENTE') {
          formData.append('pregnancy_start_date', form.value.pregnancy_start_date);
          if (form.value.expected_delivery_date) {
            formData.append('expected_delivery_date', form.value.expected_delivery_date);
          }
          if (form.value.gynecologist_name) {
            formData.append('gynecologist_name', form.value.gynecologist_name);
          }
          formData.append('is_pregnant', 'true');
        }

        // Données soignant
        if (form.value.role === 'SOIGNANT') {
          formData.append('speciality', form.value.speciality);
          formData.append('license_number', form.value.license_number);
          if (form.value.years_of_experience) {
            formData.append('years_of_experience', form.value.years_of_experience);
          }
          if (form.value.hospital_affiliation) {
            formData.append('hospital_affiliation', form.value.hospital_affiliation);
          }
          if (form.value.diploma_file) {
            formData.append('diploma_file', form.value.diploma_file);
          }
          if (form.value.license_file) {
            formData.append('license_file', form.value.license_file);
          }
          if (form.value.id_card_file) {
            formData.append('id_card_file', form.value.id_card_file);
          }
        }

        const response = await api.post('/auth/register', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        console.log(' Inscription réussie:', response.data);

        if (form.value.role === 'SOIGNANT') {
          alert(' Inscription réussie ! Votre compte est en attente de validation par l\'administrateur. Vous serez notifié par email une fois votre compte validé.');
        } else {
          alert(' Inscription réussie ! Vous pouvez maintenant vous connecter.');
        }

        router.push('/login');

      } catch (error) {
        console.error(' Erreur inscription:', error);
        if (error.response?.data?.message) {
          errorMessage.value = error.response.data.message;
        } else if (error.response?.data?.errors) {
          const errors = error.response.data.errors;
          const firstError = Object.values(errors)[0];
          errorMessage.value = Array.isArray(firstError) ? firstError[0] : 'Erreur de validation';
        } else {
          errorMessage.value = 'Erreur lors de l\'inscription. Veuillez réessayer.';
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      showPassword,
      errorMessage,
      isFormValid,
      handleFileUpload,
      handleRegister
    };
  }
};
</script>