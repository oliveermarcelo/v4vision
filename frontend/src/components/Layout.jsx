import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { 
  BarChart3, 
  Target, 
  Calendar, 
  BookOpen, 
  ChevronLeft,
  ChevronRight,
  LogOut,
  User,
  Box
} from 'lucide-react'

const menuItems = [
  { path: '/retrospectiva', icon: BarChart3, label: 'Retrospectiva 2025' },
  { path: '/estrategia', icon: Target, label: 'Estratégia 2026' },
  { path: '/gestao', icon: Calendar, label: 'Gestão Semanal' },
  { path: '/protocolos', icon: BookOpen, label: 'Protocolos' },
]

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false)
  const { user, logout, canEdit } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <aside className={`
        bg-dark-900 text-white flex flex-col transition-all duration-300
        ${collapsed ? 'w-20' : 'w-64'}
      `}>
        {/* Logo */}
        <div className="p-4 flex items-center gap-3 border-b border-dark-800">
          <div className="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center">
            <Box className="w-6 h-6" />
          </div>
          {!collapsed && (
            <div>
              <h1 className="font-bold text-lg">{user?.company_data?.name || 'V4Vision'}</h1>
              <p className="text-xs text-gray-400">Dashboard</p>
            </div>
          )}
        </div>

        {/* Menu */}
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `
                sidebar-link
                ${isActive ? 'active' : ''}
                ${collapsed ? 'justify-center px-0' : ''}
              `}
              title={collapsed ? item.label : undefined}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* User Info & Collapse */}
        <div className="p-4 border-t border-dark-800 space-y-3">
          {/* User */}
          <div className={`flex items-center gap-3 ${collapsed ? 'justify-center' : ''}`}>
            <div className="w-10 h-10 bg-dark-800 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-gray-400" />
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user?.full_name}</p>
                <p className="text-xs text-gray-400">
                  {canEdit ? 'Admin' : 'Visualizador'}
                </p>
              </div>
            )}
          </div>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className={`
              w-full flex items-center gap-3 px-4 py-2 rounded-lg
              text-gray-400 hover:text-white hover:bg-dark-800 transition-colors
              ${collapsed ? 'justify-center px-0' : ''}
            `}
            title={collapsed ? 'Sair' : undefined}
          >
            <LogOut className="w-5 h-5" />
            {!collapsed && <span>Sair</span>}
          </button>

          {/* Collapse Toggle */}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className={`
              w-full flex items-center gap-3 px-4 py-2 rounded-lg
              text-gray-400 hover:text-white hover:bg-dark-800 transition-colors
              ${collapsed ? 'justify-center px-0' : ''}
            `}
          >
            {collapsed ? (
              <ChevronRight className="w-5 h-5" />
            ) : (
              <>
                <ChevronLeft className="w-5 h-5" />
                <span>Recolher</span>
              </>
            )}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
