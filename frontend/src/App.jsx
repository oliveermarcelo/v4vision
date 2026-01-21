import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './contexts/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Retrospectiva from './pages/Retrospectiva'
import Estrategia from './pages/Estrategia'
import GestaoSemanal from './pages/GestaoSemanal'
import Protocolos from './pages/Protocolos'

function PrivateRoute({ children }) {
  const { signed, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    )
  }
  
  if (!signed) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      <Route path="/" element={
        <PrivateRoute>
          <Layout />
        </PrivateRoute>
      }>
        <Route index element={<Navigate to="/retrospectiva" replace />} />
        <Route path="retrospectiva" element={<Retrospectiva />} />
        <Route path="estrategia" element={<Estrategia />} />
        <Route path="gestao" element={<GestaoSemanal />} />
        <Route path="protocolos" element={<Protocolos />} />
      </Route>
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
