// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// Layouts
import AuthLayout from '../components/layout/AuthLayout.vue';

const routes = [
  // ============================================================
  // PAGES PUBLIQUES
  // ============================================================
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { public: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: { public: true },
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../views/ForgotPasswordView.vue'),
    meta: { public: true },
  },
  {
    path: '/reset-password/:token?',
    name: 'ResetPassword',
    component: () => import('../views/ResetPasswordView.vue'),
    meta: { public: true },
  },

  // ============================================================
  // ROUTES PROTÉGÉES (/app)
  // ============================================================
  {
    path: '/app',
    component: AuthLayout,
    meta: { requiresAuth: true },
    children: [
      // ============================================================
      // DASHBOARD
      // ============================================================
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/DashboardView.vue'),
        meta: { roles: ['PATIENTE', 'SOIGNANT', 'ADMIN'] },
      },

      // ============================================================
      // PATIENT - Routes
      // ============================================================
      {
        path: 'patient/pregnancies',
        name: 'Pregnancies',
        component: () => import('../views/patient/PregnanciesView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/pregnancy/:id?',
        name: 'Pregnancy',
        component: () => import('../views/patient/PregnancyView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/pregnancy/create',
        name: 'PregnancyCreate',
        component: () => import('../views/patient/PregnancyCreateView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/appointments',
        name: 'PatientAppointments',
        component: () => import('../views/patient/AppointmentsView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/appointment/create',
        name: 'PatientAppointmentCreate',
        component: () => import('../views/patient/AppointmentCreateView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/records',
        name: 'MedicalRecords',
        component: () => import('../views/patient/MedicalRecordsView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/records/:id',
        name: 'MedicalRecordDetail',
        component: () => import('../views/patient/MedicalRecordDetailView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/messages',
        name: 'PatientMessages',
        component: () => import('../views/patient/MessagesView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/profile',
        name: 'PatientProfile',
        component: () => import('../views/patient/ProfileView.vue'),
        meta: { roles: ['PATIENTE'] },
      },
      {
        path: 'patient/settings',
        name: 'PatientSettings',
        component: () => import('../views/patient/SettingsView.vue'),
        meta: { roles: ['PATIENTE'] },
      },

      // ============================================================
      // DOCTOR - Routes
      // ============================================================
      {
        path: 'doctor/dashboard',
        name: 'DoctorDashboard',
        component: () => import('../views/doctor/DashboardView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/patients',
        name: 'DoctorPatients',
        component: () => import('../views/doctor/PatientsView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/patients/:id',
        name: 'DoctorPatientDetail',
        component: () => import('../views/doctor/PatientDetailView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/appointments',
        name: 'DoctorAppointments',
        component: () => import('../views/doctor/AppointmentsView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/consultations',
        name: 'DoctorConsultations',
        component: () => import('../views/doctor/ConsultationsView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/schedule',
        name: 'DoctorSchedule',
        component: () => import('../views/doctor/ScheduleView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/messages',
        name: 'DoctorMessages',
        component: () => import('../views/doctor/MessagesView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/profile',
        name: 'DoctorProfile',
        component: () => import('../views/doctor/ProfileView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },
      {
        path: 'doctor/settings',
        name: 'DoctorSettings',
        component: () => import('../views/doctor/SettingsView.vue'),
        meta: { roles: ['SOIGNANT'] },
      },

      // ============================================================
      // ADMIN - Routes
      // ============================================================
      {
        path: 'admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/DashboardView.vue'),
        meta: { roles: ['ADMIN'] },
      },
      {
        path: 'admin/users',
        name: 'AdminUsers',
        component: () => import('../views/admin/UsersView.vue'),
        meta: { roles: ['ADMIN'] },
      },
      {
        path: 'admin/users/:id',
        name: 'AdminUserDetail',
        component: () => import('../views/admin/UserDetailView.vue'),
        meta: { roles: ['ADMIN'] },
      },
      {
        path: 'admin/stats',
        name: 'AdminStats',
        component: () => import('../views/admin/StatsView.vue'),
        meta: { roles: ['ADMIN'] },
      },
      {
        path: 'admin/settings',
        name: 'AdminSettings',
        component: () => import('../views/admin/SettingsView.vue'),
        meta: { roles: ['ADMIN'] },
      },
      {
        path: 'admin/logs',
        name: 'AdminLogs',
        component: () => import('../views/admin/LogsView.vue'),
        meta: { roles: ['ADMIN'] },
      },
    ],
  },

  // ============================================================
  // PAGE 404 - NOT FOUND
  // ============================================================
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ============================================================
// GARDE DE NAVIGATION
// ============================================================
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Restaurer depuis localStorage si nécessaire
  if (!authStore.isAuthenticated) {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('userRole');
    const user = localStorage.getItem('user');
    
    if (token && userRole && user) {
      try {
        authStore.setToken(token);
        authStore.setUser(JSON.parse(user));
        console.log('✅ Store restauré depuis localStorage');
      } catch (e) {
        console.warn('⚠️ Erreur restauration store:', e);
      }
    }
  }

  // === ROUTES PUBLIQUES ===
  if (to.meta.public) {
    if (authStore.isAuthenticated && (to.path === '/' || to.path === '/login' || to.path === '/register')) {
      next('/app/dashboard');
      return;
    }
    next();
    return;
  }

  // === ROUTES PROTÉGÉES ===
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      next('/login');
      return;
    }

    if (to.meta.roles && to.meta.roles.length > 0) {
      const userRole = authStore.userRole;
      if (!to.meta.roles.includes(userRole)) {
        next('/app/dashboard');
        return;
      }
    }
    next();
    return;
  }

  next();
});

export default router;