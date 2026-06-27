 <!-- src/views/HomeView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-rose-50 via-white to-pink-50">
    <!-- Navigation -->
    <nav class="bg-white/80 backdrop-blur-md shadow-sm fixed w-full top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-2">
            <Heart class="w-8 h-8 text-rose-500" />
            <span class="text-xl font-bold text-rose-700">Suivi Grossesse</span>
          </div>
          <div class="flex items-center gap-4">
            <router-link to="/login" class="text-gray-600 hover:text-rose-600 transition font-medium">
              Connexion
            </router-link>
            <router-link to="/register" class="bg-rose-500 text-white px-4 py-2 rounded-lg hover:bg-rose-600 transition font-medium">
              S'inscrire
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-24 pb-16 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 class="text-4xl md:text-5xl font-bold text-gray-800 leading-tight">
              Suivez votre grossesse
              <span class="text-rose-500">en toute sérénité</span>
            </h1>
            <p class="text-lg text-gray-600 mt-4">
              Une plateforme complète pour suivre votre grossesse, 
              communiquer avec votre médecin et accéder à tous vos 
              documents médicaux en un seul endroit.
            </p>
            <div class="flex flex-wrap gap-4 mt-8">
              <router-link to="/register" class="bg-rose-500 text-white px-8 py-3 rounded-lg hover:bg-rose-600 transition font-medium flex items-center gap-2">
                <UserPlus class="w-5 h-5" /> Créer un compte
              </router-link>
              <router-link to="/login" class="border-2 border-rose-500 text-rose-500 px-8 py-3 rounded-lg hover:bg-rose-50 transition font-medium">
                Se connecter
              </router-link>
            </div>
            <div class="flex items-center gap-6 mt-6 text-sm text-gray-500">
              <span class="flex items-center gap-1"> Gratuit</span>
              <span class="flex items-center gap-1"> Sécurisé</span>
              <span class="flex items-center gap-1"> Médical</span>
            </div>
          </div>
          <div class="flex justify-center">
            <div class="relative">
              <div class="w-80 h-80 bg-gradient-to-br from-rose-100 to-pink-200 rounded-full flex items-center justify-center">
                <Heart class="w-40 h-40 text-rose-400/60" />
              </div>
              <div class="absolute -top-4 -right-4 bg-white rounded-xl p-3 shadow-lg border border-rose-100">
                <div class="flex items-center gap-2">
                  <Baby class="w-6 h-6 text-rose-500" />
                  <span class="text-sm font-medium text-gray-700">Grossesse</span>
                </div>
              </div>
              <div class="absolute -bottom-4 -left-4 bg-white rounded-xl p-3 shadow-lg border border-rose-100">
                <div class="flex items-center gap-2">
                  <Calendar class="w-6 h-6 text-blue-500" />
                  <span class="text-sm font-medium text-gray-700">Suivi</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 px-4 bg-white/50">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">
          Une plateforme complète pour <span class="text-rose-500">vous accompagner</span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 hover:shadow-lg transition">
            <div class="w-14 h-14 bg-rose-100 rounded-lg flex items-center justify-center mb-4">
              <Baby class="w-7 h-7 text-rose-500" />
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Suivi de grossesse</h3>
            <p class="text-gray-600">
              Suivez l'évolution de votre grossesse semaine après semaine,
              avec des conseils personnalisés.
            </p>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 hover:shadow-lg transition">
            <div class="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <Calendar class="w-7 h-7 text-blue-500" />
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Rendez-vous</h3>
            <p class="text-gray-600">
              Prenez et gérez vos rendez-vous médicaux facilement,
              avec rappels automatiques.
            </p>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100 hover:shadow-lg transition">
            <div class="w-14 h-14 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <MessageCircle class="w-7 h-7 text-green-500" />
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Messagerie</h3>
            <p class="text-gray-600">
              Communiquez directement avec votre médecin ou sage-femme
              en toute sécurité.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-16 px-4">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">
          Comment ça <span class="text-rose-500">fonctionne</span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="w-16 h-16 bg-rose-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">1</div>
            <h3 class="font-semibold text-gray-800 mb-2">Créez votre compte</h3>
            <p class="text-sm text-gray-500">Inscrivez-vous en quelques clics</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-rose-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">2</div>
            <h3 class="font-semibold text-gray-800 mb-2">Suivez votre grossesse</h3>
            <p class="text-sm text-gray-500">Entrez vos données et suivez l'évolution</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-rose-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">3</div>
            <h3 class="font-semibold text-gray-800 mb-2">Prenez rendez-vous</h3>
            <p class="text-sm text-gray-500">Trouvez et réservez des créneaux</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-rose-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">4</div>
            <h3 class="font-semibold text-gray-800 mb-2">Restez connectée</h3>
            <p class="text-sm text-gray-500">Communiquez avec votre médecin</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-16 px-4 bg-rose-500/5">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <p class="text-4xl font-bold text-rose-500">500+</p>
            <p class="text-gray-600 mt-1">Grossesses suivies</p>
          </div>
          <div>
            <p class="text-4xl font-bold text-rose-500">1 200+</p>
            <p class="text-gray-600 mt-1">Rendez-vous effectués</p>
          </div>
          <div>
            <p class="text-4xl font-bold text-rose-500">150+</p>
            <p class="text-gray-600 mt-1">Médecins inscrits</p>
          </div>
          <div>
            <p class="text-4xl font-bold text-rose-500">98%</p>
            <p class="text-gray-600 mt-1">Satisfaction</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="py-16 px-4">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">
          Ce qu'en disent <span class="text-rose-500">nos utilisatrices</span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-rose-100 rounded-full flex items-center justify-center text-rose-600 font-bold text-lg">MD</div>
              <div>
                <h4 class="font-semibold text-gray-800">Marie Diop</h4>
                <p class="text-sm text-gray-500">Patiente</p>
              </div>
            </div>
            <p class="text-gray-600 text-sm italic">
              "Cette plateforme m'a énormément aidée tout au long de ma grossesse.
              Je pouvais suivre l'évolution et communiquer facilement avec mon médecin."
            </p>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-lg">JM</div>
              <div>
                <h4 class="font-semibold text-gray-800">Dr. Jean Martin</h4>
                <p class="text-sm text-gray-500">Gynécologue</p>
              </div>
            </div>
            <p class="text-gray-600 text-sm italic">
              "Un outil indispensable pour le suivi de mes patientes.
              La messagerie simplifie énormément la communication."
            </p>
          </div>
          <div class="bg-white rounded-xl p-6 shadow-sm border border-rose-100">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold text-lg">FS</div>
              <div>
                <h4 class="font-semibold text-gray-800">Fatou Sow</h4>
                <p class="text-sm text-gray-500">Sage-femme</p>
              </div>
            </div>
            <p class="text-gray-600 text-sm italic">
              "Je recommande cette plateforme à toutes les futures mamans.
              Le suivi est simple et efficace."
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-16 px-4 bg-gradient-to-r from-rose-500 to-pink-500">
      <div class="max-w-7xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-white mb-4">
          Prête à commencer votre suivi ?
        </h2>
        <p class="text-white/80 text-lg mb-8 max-w-2xl mx-auto">
          Rejoignez des milliers de femmes qui suivent leur grossesse
          en toute sérénité.
        </p>
        <router-link to="/register" class="bg-white text-rose-500 px-8 py-3 rounded-lg hover:bg-rose-50 transition font-medium inline-flex items-center gap-2">
          <UserPlus class="w-5 h-5" /> Créer mon compte
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 py-8 px-4">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <div class="flex items-center gap-2 mb-4">
            <Heart class="w-6 h-6 text-rose-500" />
            <span class="text-white font-bold">Suivi Grossesse</span>
          </div>
          <p class="text-sm">Suivez votre grossesse en toute sérénité</p>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-3">Navigation</h4>
          <ul class="space-y-2 text-sm">
            <li><router-link to="/" class="hover:text-white transition">Accueil</router-link></li>
            <li><router-link to="/login" class="hover:text-white transition">Connexion</router-link></li>
            <li><router-link to="/register" class="hover:text-white transition">Inscription</router-link></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-3">Liens utiles</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-white transition">À propos</a></li>
            <li><a href="#" class="hover:text-white transition">Contact</a></li>
            <li><a href="#" class="hover:text-white transition">FAQ</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-3">Légal</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="hover:text-white transition">Mentions légales</a></li>
            <li><a href="#" class="hover:text-white transition">Confidentialité</a></li>
            <li><a href="#" class="hover:text-white transition">CGU</a></li>
          </ul>
        </div>
      </div>
      <div class="max-w-7xl mx-auto border-t border-gray-800 mt-8 pt-8 text-center text-sm">
        <p>© 2025 Suivi Grossesse. Tous droits réservés.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { Heart, UserPlus, Baby, Calendar, MessageCircle } from 'lucide-vue-next';

export default {
  name: 'HomeView',
  components: {
    Heart,
    UserPlus,
    Baby,
    Calendar,
    MessageCircle
  }
};
</script>

<style scoped>
/* Animation douce pour les cartes */
.hover\:shadow-lg {
  transition: all 0.3s ease;
}

/* Animation pour les nombres */
.text-4xl {
  font-variant-numeric: tabular-nums;
}
</style>