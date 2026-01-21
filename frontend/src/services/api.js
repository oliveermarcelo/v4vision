import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refresh = localStorage.getItem('@v4vision:refresh')
        if (refresh) {
          const response = await axios.post('/api/auth/refresh/', { refresh })
          const { access } = response.data
          
          localStorage.setItem('@v4vision:token', access)
          api.defaults.headers.common['Authorization'] = `Bearer ${access}`
          originalRequest.headers['Authorization'] = `Bearer ${access}`
          
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh falhou, fazer logout
        localStorage.removeItem('@v4vision:token')
        localStorage.removeItem('@v4vision:refresh')
        localStorage.removeItem('@v4vision:user')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

export default api

// Serviços específicos
export const authService = {
  login: (email, password) => api.post('/api/auth/login/', { email, password }),
  logout: (refresh) => api.post('/api/auth/logout/', { refresh }),
  refresh: (refresh) => api.post('/api/auth/refresh/', { refresh }),
}

export const userService = {
  me: () => api.get('/api/users/me/'),
  update: (data) => api.patch('/api/users/me/', data),
  changePassword: (data) => api.post('/api/users/change_password/', data),
}

export const dashboardService = {
  // Retrospectiva
  getRetrospectiva: (ano) => api.get(`/api/receitas/retrospectiva/?ano=${ano}`),
  getComparativoVendedores: (ano) => api.get(`/api/receitas/comparativo_vendedores/?ano=${ano}`),
  
  // Receitas
  getReceitas: (params) => api.get('/api/receitas/', { params }),
  createReceita: (data) => api.post('/api/receitas/', data),
  updateReceita: (id, data) => api.patch(`/api/receitas/${id}/`, data),
  deleteReceita: (id) => api.delete(`/api/receitas/${id}/`),
  
  // Estratégia
  getEstrategias: (params) => api.get('/api/estrategias/', { params }),
  createEstrategia: (data) => api.post('/api/estrategias/', data),
  updateEstrategia: (id, data) => api.patch(`/api/estrategias/${id}/`, data),
  setInvestimentos: (id, data) => api.post(`/api/estrategias/${id}/set_investimentos/`, data),
  
  // Gestão Semanal
  getGestaoSemanal: (params) => api.get('/api/gestao-semanal/', { params }),
  createGestaoSemanal: (data) => api.post('/api/gestao-semanal/', data),
  updateGestaoSemanal: (id, data) => api.patch(`/api/gestao-semanal/${id}/`, data),
  
  // Protocolos
  getProtocolos: () => api.get('/api/protocolos/'),
  createProtocolo: (data) => api.post('/api/protocolos/', data),
  updateProtocolo: (id, data) => api.patch(`/api/protocolos/${id}/`, data),
  
  // Vendedores
  getVendedores: () => api.get('/api/vendedores/'),
  createVendedor: (data) => api.post('/api/vendedores/', data),
}
