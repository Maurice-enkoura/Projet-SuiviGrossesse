// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // ===== ÉTAT =====
  // Charger depuis localStorage au démarrage
  const storedToken = localStorage.getItem('token') || null
  const storedUser = localStorage.getItem('user') || null
  const storedRole = localStorage.getItem('userRole') || null

  const user = ref(storedUser ? JSON.parse(storedUser) : null)
  const token = ref(storedToken)
  const isAuthenticated = ref(!!storedToken)
  const userRole = ref(storedRole)

  // ===== GETTERS =====
  const getUser = computed(() => user.value)
  const getToken = computed(() => token.value)
  const getRole = computed(() => userRole.value)

  // ===== ACTIONS =====
  function setUser(userData) {
    user.value = userData
    userRole.value = userData?.role || null
    isAuthenticated.value = true
    
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
      if (userData.role) {
        localStorage.setItem('userRole', userData.role)
      }
    }
  }

  function setToken(newToken) {
    token.value = newToken
    isAuthenticated.value = true
    
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  function login(userData, userToken) {
    console.log('🔐 Login - Données reçues:', { userData, userToken })
    setUser(userData)
    setToken(userToken)
    console.log('🔐 Login - Après setUser:', {
      user: user.value,
      role: userRole.value,
      isAuthenticated: isAuthenticated.value
    })
  }

  function logout() {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    userRole.value = null
    
    localStorage.removeItem('token')
    localStorage.removeItem('userRole')
    localStorage.removeItem('user')
  }

  function updateUser(userData) {
    user.value = { ...user.value, ...userData }
    if (userData.role) {
      userRole.value = userData.role
      localStorage.setItem('userRole', userData.role)
    }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  return {
    user,
    token,
    isAuthenticated,
    userRole,
    getUser,
    getToken,
    getRole,
    setUser,
    setToken,
    login,
    logout,
    updateUser
  }
})