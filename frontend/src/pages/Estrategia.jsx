import { useState, useEffect } from 'react'
import { dashboardService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import { AlertTriangle } from 'lucide-react'

const meses = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

export default function Estrategia() {
  const [estrategias, setEstrategias] = useState([])
  const [cenario, setCenario] = useState('conservador')
  const [loading, setLoading] = useState(true)
  const { canEdit } = useAuth()

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const response = await dashboardService.getEstrategias({ ano: 2026 })
      setEstrategias(response.data.results || response.data)
    } catch (error) {
      console.error('Erro ao carregar estratégias:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value)
  }

  const estrategiaAtual = estrategias.find(e => e.cenario === cenario)

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
        <h1 className="text-2xl font-bold text-gray-900">Estratégia 2026</h1>
        <p className="text-gray-500">Planejamento e roadmap de investimentos</p>
      </div>

      {/* Seletor de Cenário */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-gray-500">Selecionar Cenário</span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setCenario('conservador')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                cenario === 'conservador' 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Conservador
            </button>
            <button
              onClick={() => setCenario('ousado')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                cenario === 'ousado' 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Ousado
            </button>
          </div>
        </div>

        {/* Métricas */}
        {estrategiaAtual && (
          <div className="grid grid-cols-2 gap-6 mt-6">
            <div>
              <p className="text-gray-500 text-sm">Orçamento Total</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatCurrency(estrategiaAtual.orcamento_total)}
              </p>
            </div>
            <div>
              <p className="text-gray-500 text-sm">Receita Projetada</p>
              <p className="text-2xl font-bold text-primary-500">
                {formatCurrency(estrategiaAtual.receita_projetada)}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Roadmap de Investimento */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">Roadmap de Investimento Mensal</h2>
        
        {estrategiaAtual?.investimentos_mensais?.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {meses.map((mes, index) => {
              const investimento = estrategiaAtual.investimentos_mensais.find(
                inv => inv.mes === index + 1
              )
              const valor = investimento?.valor || 0
              const maxValor = Math.max(
                ...estrategiaAtual.investimentos_mensais.map(i => Number(i.valor))
              )
              const isMax = Number(valor) === maxValor && maxValor > 0
              
              return (
                <div 
                  key={mes}
                  className={`p-4 rounded-lg border ${
                    isMax 
                      ? 'border-primary-300 bg-primary-50' 
                      : 'border-gray-200 bg-white'
                  }`}
                >
                  <p className="text-gray-500 text-sm">{mes}</p>
                  <p className={`text-lg font-bold ${isMax ? 'text-primary-500' : 'text-gray-900'}`}>
                    {formatCurrency(valor)}
                  </p>
                </div>
              )
            })}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            Nenhum investimento planejado para este cenário
          </p>
        )}
      </div>

      {/* Regra de Ouro */}
      {estrategiaAtual && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h3 className="font-bold text-amber-800">REGRA DE OURO</h3>
              <p className="text-amber-700 mt-1">
                Se ROAS &lt; <strong>{estrategiaAtual.roas_minimo}</strong>, congelar investimento.
              </p>
              <p className="text-amber-600 text-sm mt-2">
                Esta regra protege o orçamento contra campanhas de baixa performance.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Mensagem se não houver dados */}
      {!estrategiaAtual && (
        <div className="card text-center py-12">
          <p className="text-gray-500">
            Nenhuma estratégia cadastrada para o cenário {cenario}.
          </p>
          {canEdit && (
            <button className="btn-primary mt-4">
              Criar Estratégia
            </button>
          )}
        </div>
      )}
    </div>
  )
}
