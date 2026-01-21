import { useState, useEffect } from 'react'
import { dashboardService } from '../services/api'
import { Clock, Target, MessageSquare, FileText } from 'lucide-react'

const iconMap = {
  clock: Clock,
  target: Target,
  'message-square': MessageSquare,
  default: FileText
}

const colorMap = {
  orange: 'bg-orange-100 text-orange-500',
  green: 'bg-green-100 text-green-500',
  blue: 'bg-blue-100 text-blue-500',
  purple: 'bg-purple-100 text-purple-500',
}

export default function Protocolos() {
  const [protocolos, setProtocolos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const response = await dashboardService.getProtocolos()
      setProtocolos(response.data.results || response.data)
    } catch (error) {
      console.error('Erro ao carregar protocolos:', error)
    } finally {
      setLoading(false)
    }
  }

  // Dados padrão caso não haja protocolos cadastrados
  const defaultProtocolos = [
    {
      id: 1,
      tipo: 'sla',
      titulo: 'SLA',
      descricao: 'Atendimento em 30 min',
      icone: 'clock',
      cor: 'orange'
    },
    {
      id: 2,
      tipo: 'foco',
      titulo: 'Foco',
      descricao: 'Mídia gera Pipeline, Vendedor fecha',
      icone: 'target',
      cor: 'green'
    },
    {
      id: 3,
      tipo: 'feedback',
      titulo: 'Feedback',
      descricao: 'Relatório Mensal Obrigatório',
      icone: 'message-square',
      cor: 'blue'
    }
  ]

  const displayProtocolos = protocolos.length > 0 ? protocolos : defaultProtocolos

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Protocolos</h1>
        <p className="text-gray-500">Regras operacionais para o time comercial</p>
      </div>

      {/* Cards de Protocolos */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {displayProtocolos.map((protocolo) => {
          const IconComponent = iconMap[protocolo.icone] || iconMap.default
          const colorClass = colorMap[protocolo.cor] || colorMap.orange
          
          return (
            <div key={protocolo.id} className="card hover:shadow-md transition-shadow">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-4 ${colorClass}`}>
                <IconComponent className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-gray-900">{protocolo.titulo}</h3>
              <p className="text-gray-500 mt-1">{protocolo.descricao}</p>
            </div>
          )
        })}
      </div>

      {/* Resumo dos Protocolos */}
      <div className="bg-dark-900 rounded-xl p-6 text-white">
        <h2 className="text-lg font-semibold mb-4">Resumo dos Protocolos</h2>
        
        <ul className="space-y-3">
          <li className="flex items-start gap-3">
            <span className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></span>
            <span className="text-gray-300">
              Todos os leads devem ser contatados em no máximo 30 minutos após a entrada.
            </span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
            <span className="text-gray-300">
              Marketing é responsável por gerar pipeline qualificado; Vendas é responsável por converter.
            </span>
          </li>
          <li className="flex items-start gap-3">
            <span className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></span>
            <span className="text-gray-300">
              Relatório mensal de performance é obrigatório para alinhamento entre equipes.
            </span>
          </li>
        </ul>
      </div>

      {/* Mensagem se não houver protocolos cadastrados */}
      {protocolos.length === 0 && (
        <div className="text-center text-gray-500 text-sm">
          <p>Exibindo protocolos padrão. Personalize cadastrando seus próprios protocolos.</p>
        </div>
      )}
    </div>
  )
}
