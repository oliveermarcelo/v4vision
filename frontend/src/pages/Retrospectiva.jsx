import { useState, useEffect } from 'react'
import { dashboardService } from '../services/api'
import { DollarSign, TrendingUp, Target, Sparkles } from 'lucide-react'
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, ComposedChart, Legend
} from 'recharts'

const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

export default function Retrospectiva() {
  const [data, setData] = useState(null)
  const [comparativo, setComparativo] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [retroResponse, compResponse] = await Promise.all([
        dashboardService.getRetrospectiva(2025),
        dashboardService.getComparativoVendedores(2025)
      ])
      setData(retroResponse.data)
      setComparativo(compResponse.data)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
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

  const chartData = data?.receitas_mensais?.map(item => ({
    mes: meses[item.mes - 1],
    receita: Number(item.receita),
    roas: item.roas
  })) || []

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
        <h1 className="text-2xl font-bold text-gray-900">Retrospectiva 2025</h1>
        <p className="text-gray-500">Análise completa do desempenho anual</p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-primary-500" />
            </div>
            <span className="text-gray-500">Receita Total</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {formatCurrency(data?.receita_total || 0)}
          </p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-green-500" />
            </div>
            <span className="text-gray-500">ROAS Global</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {data?.roas_global?.toFixed(2) || '0.00'}
          </p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Target className="w-5 h-5 text-blue-500" />
            </div>
            <span className="text-gray-500">Investimento</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">
            {formatCurrency(data?.investimento_total || 0)}
          </p>
        </div>
      </div>

      {/* Gráfico Receita Mensal */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">Receita Mensal 2025</h2>
          {data?.mes_pico && (
            <span className="flex items-center gap-2 text-sm bg-primary-100 text-primary-600 px-3 py-1 rounded-full">
              <Sparkles className="w-4 h-4" />
              Pico: {data.mes_pico.mes_nome}
            </span>
          )}
        </div>
        
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="mes" tick={{ fill: '#6b7280' }} />
              <YAxis 
                yAxisId="left"
                tick={{ fill: '#6b7280' }}
                tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
              />
              <YAxis 
                yAxisId="right"
                orientation="right"
                tick={{ fill: '#6b7280' }}
                domain={[0, 'auto']}
              />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'receita' ? formatCurrency(value) : value.toFixed(2),
                  name === 'receita' ? 'Receita' : 'ROAS'
                ]}
              />
              <Legend />
              <Bar 
                yAxisId="left"
                dataKey="receita" 
                fill="#f97316" 
                radius={[4, 4, 0, 0]}
                name="Receita"
              />
              <Line 
                yAxisId="right"
                type="monotone" 
                dataKey="roas" 
                stroke="#22c55e" 
                strokeWidth={2}
                dot={{ fill: '#22c55e' }}
                name="ROAS"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Comparativo Vendedores */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">Comparativo Vendedores</h2>
        
        <div className="space-y-4">
          {comparativo.map((item, index) => {
            const maxValue = Math.max(...comparativo.map(v => Number(v.total)))
            const percentage = (Number(item.total) / maxValue) * 100
            
            return (
              <div key={index}>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-700">{item.vendedor}</span>
                  <span className="font-semibold text-primary-500">
                    {formatCurrency(item.total)}
                  </span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-3">
                  <div 
                    className={`h-3 rounded-full ${index === 0 ? 'bg-primary-500' : 'bg-gray-400'}`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            )
          })}
          
          {comparativo.length === 0 && (
            <p className="text-gray-500 text-center py-4">
              Nenhum dado de vendedores disponível
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
