// src/services/api.js
import axios from 'axios'

// ⚠️ IMPORTANT: L'URL doit correspondre à celle du backend
// Les URLs du backend sont: /api/v1/auth/login, /api/v1/patient/pregnancies, etc.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000,
})

// Intercepteur pour ajouter le token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    console.log(` ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`)
    return config
  },
  (error) => {
    console.error(' Erreur de requête:', error)
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les réponses
api.interceptors.response.use(
  (response) => {
    console.log(` ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    if (error.response) {
      console.error(' Erreur réponse:', error.response.status, error.response.data)
      
      if (error.response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        localStorage.removeItem('userRole')
        window.location.href = '/login'
      }
    } else if (error.request) {
      console.error(' Pas de réponse du serveur:', error.request)
    } else {
      console.error(' Erreur:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api