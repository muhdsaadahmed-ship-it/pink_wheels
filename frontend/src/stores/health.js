import { defineStore } from 'pinia'
import api from '../services/api'

export const useHealthStore = defineStore('health', {
  state: () => ({
    status: null,
    database: null,
    loading: false,
    error: null,
  }),
  actions: {
    async check() {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get('/api/health')
        this.status = data.status
        this.database = data.database
      } catch (err) {
        this.status = 'unreachable'
        this.database = 'unknown'
        this.error = err.message
      } finally {
        this.loading = false
      }
      return this.status
    },
  },
})
