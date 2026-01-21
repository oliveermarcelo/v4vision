import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const AuthContext = createContext({})

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('@v4vision:token')
    const storedUser = localStorage.getItem('@v4vision:user')
    
    if (token && storedUser) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      setUser(JSON.parse(storedUser))
    }
    
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/auth/login/', { email, password })
      const { access, refresh } = response.data
      
      localStorage.setItem('@v4vision:token', access)
      localStorage.setItem('@v4vision:refresh', refresh)
      
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`
      
      // Buscar dados do usuário
      const userResponse = await api.get('/api/users/me/')
      const userData = userResponse.data
      
      localStorage.setItem('@v4vision:user', JSON.stringify(userData))
      setUser(userData)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Erro ao fazer login'
      }
    }
  }

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('@v4vision:refresh')
      if (refresh) {
        await api.post('/api/auth/logout/', { refresh })
      }
    } catch (error) {
      console.error('Erro no logout:', error)
    } finally {
      localStorage.removeItem('@v4vision:token')
      localStorage.removeItem('@v4vision:refresh')
      localStorage.removeItem('@v4vision:user')
      delete api.defaults.headers.common['Authorization']
      setUser(null)
    }
  }

  const updateUser = (data) => {
    const updatedUser = { ...user, ...data }
    localStorage.setItem('@v4vision:user', JSON.stringify(updatedUser))
    setUser(updatedUser)
  }

  return (
    <AuthContext.Provider value={{ 
      user, 
      loading, 
      signed: !!user,
      canEdit: user?.can_edit || false,
      login, 
      logout,
      updateUser 
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
