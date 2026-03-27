import { defineStore } from 'pinia'
import axios from 'axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('access_token') || null,
    loading: false,
    error: null,
  }),
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post('http://localhost:8000/api/auth/login/', {
          email,
          password,
        })

        const { access_token, refresh_token, user } = response.data

        this.token = access_token
        this.user = user
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        localStorage.setItem('user', JSON.stringify(user))

        // Redirect based on role
        if (user.role === 'CUSTOMER') router.push('/pets')
        else if (user.role === 'SUPPORT') router.push('/support/claims')
        else if (user.role === 'ADMIN') router.push('/admin')
      } catch (err) {
        this.error = 'Invalid credentials'
        throw err
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      router.push('/login')
    },
  },
})
