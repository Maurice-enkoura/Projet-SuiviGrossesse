// src/utils/helpers.js
import dayjs from 'dayjs'
import 'dayjs/locale/fr'

dayjs.locale('fr')

export const formatDate = (date, format = 'DD/MM/YYYY') => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

export const formatDateTime = (date, format = 'DD/MM/YYYY HH:mm') => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

export const formatPrice = (price) => {
  if (!price) return '0 FCFA'
  return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA'
}

export const getInitials = (name) => {
  if (!name) return 'U'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

export const getStatusColor = (status) => {
  const colors = {
    active: 'bg-green-100 text-green-700',
    pending: 'bg-yellow-100 text-yellow-700',
    completed: 'bg-blue-100 text-blue-700',
    cancelled: 'bg-red-100 text-red-700',
    expired: 'bg-gray-100 text-gray-700',
  }
  return colors[status] || 'bg-gray-100 text-gray-700'
}

export const getStatusLabel = (status) => {
  const labels = {
    active: 'Actif',
    pending: 'En attente',
    completed: 'Terminé',
    cancelled: 'Annulé',
    expired: 'Expiré',
  }
  return labels[status] || status
}

export const truncateText = (text, length = 50) => {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}