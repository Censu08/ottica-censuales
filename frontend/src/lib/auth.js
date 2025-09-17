import api from './api'
import Cookies from 'js-cookie'

export const authService = {
  async login(credentials) {
    const response = await api.post('/auth/login/', credentials)
    const { access, refresh, user } = response.data
    
    // Salva token nei cookie
    Cookies.set('access_token', access, { expires: 1 }) // 1 giorno
    Cookies.set('refresh_token', refresh, { expires: 7 }) // 7 giorni
    
    return { user, access, refresh }
  },

  async register(userData) {
    const response = await api.post('/auth/register/', userData)
    const { access, refresh, user } = response.data
    
    Cookies.set('access_token', access, { expires: 1 })
    Cookies.set('refresh_token', refresh, { expires: 7 })
    
    return { user, access, refresh }
  },

  logout() {
    Cookies.remove('access_token')
    Cookies.remove('refresh_token')
  },

  async getProfile() {
    const response = await api.get('/auth/profile/')
    return response.data
  },

  isAuthenticated() {
    return !!Cookies.get('access_token')
  },
}