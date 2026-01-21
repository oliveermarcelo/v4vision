import { useState, useEffect } from 'react'
import { dashboardService } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import { Save, Loader2 } from 'lucide-react'

const mesesOptions = [
  { value: 1, label: 'Janeiro' },
  { value: 2, label: 'Fevereiro' },
  { value: 3, label: 'Março' },
  { value: 4, label: 'Abril' },
  { value: 5, label: 'Maio' },
  { value: 6, label: 'Junho' },
  { value: 7, label: 'Julho' },
  { value: 8, label: 'Agosto' },
  { value: 9, label: 'Setembro' },
  { value: 10, label: 'Outubro' },
  { value: 11, label: 'Novembro' },
  { value: 12, label: 'Dezembro' },
]

const semanasOptions = [
  { value: 1, label: 'Semana 1' },
  { value: 2, label: 'Semana 2' },
  { value: 3, label: 'Semana 3' },
  { value: 4, label: 'Semana 4' },
  { value: 5, label: 'Semana 5' },
]

export default function GestaoSemanal() {
  const [registros, setRegistros] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const { canEdit } = useAuth()
  
  const [form, setForm] = useState({
    ano: 2025,
    mes: 1,
    semana: 1,
    investimento: '',
    leads: '',
    vendas: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const response = await dashboardService.getGestaoSemanal({ ano: 2025 })
      setRegistros(response.data.results || response.data)
    } catch (error) {
      console.error('Erro ao carregar gestão semanal:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!canEdit) return
    
    setSaving(true)
    try {
      await dashboardService.createGestaoSemanal({
        ...form,
        investimento: parseFloat(form.investimento),
        leads: parseInt(form.leads),
        vendas: parseFloat(form.vendas)
      })
      await loadData()
      setForm({
        ...form,
        investimento: '',
        leads: '',
        vendas: ''
      })
    } catch (error) {
      console.error('Erro ao salvar:', error)
      alert('Erro ao salvar registro')
    } finally {
      setSaving(false)
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
        <h1 className="text-2xl font-bold text-gray-900">Gestão Semanal</h1>
        <p className="text-gray-500">Ferramenta de acompanhamento operacional</p>
      </div>

      {/* Formulário */}
      {canEdit && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Registrar Dados da Semana</h2>
          
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Mês</label>
                <select
                  value={form.mes}
                  onChange={(e) => setForm({ ...form, mes: parseInt(e.target.value) })}
                  className="input"
                >
                  {mesesOptions.map(m => (
                    <option key={m.value} value={m.value}>{m.label}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm text-gray-600 mb-1">Semana</label>
                <select
                  value={form.semana}
                  onChange={(e) => setForm({ ...form, semana: parseInt(e.target.value) })}
                  className="input"
                >
                  {semanasOptions.map(s => (
                    <option key={s.value} value={s.value}>{s.label}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm text-gray-600 mb-1">Investimento (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={form.investimento}
                  onChange={(e) => setForm({ ...form, investimento: e.target.value })}
                  className="input"
                  placeholder="0,00"
                  required
                />
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Leads (Qtd)</label>
                <input
                  type="number"
                  value={form.leads}
                  onChange={(e) => setForm({ ...form, leads: e.target.value })}
                  className="input"
                  placeholder="0"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-600 mb-1">Vendas (R$)</label>
                <input
                  type="number"
                  step="0.01"
                  value={form.vendas}
                  onChange={(e) => setForm({ ...form, vendas: e.target.value })}
                  className="input"
                  placeholder="0,00"
                  required
                />
              </div>
              
              <div className="flex items-end">
                <button
                  type="submit"
                  disabled={saving}
                  className="w-full btn-primary flex items-center justify-center gap-2"
                >
                  {saving ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Salvando...
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      Salvar Dados
                    </>
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>
      )}

      {/* Tabela de Registros */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Registros Salvos</h2>
        
        {registros.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-gray-600 font-medium">Mês</th>
                  <th className="text-left py-3 px-4 text-gray-600 font-medium">Semana</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Investimento</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Leads</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Vendas</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">ROAS</th>
                </tr>
              </thead>
              <tbody>
                {registros.map((registro) => (
                  <tr key={registro.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4">{registro.mes_nome}</td>
                    <td className="py-3 px-4">{registro.semana_nome}</td>
                    <td className="py-3 px-4 text-right">{formatCurrency(registro.investimento)}</td>
                    <td className="py-3 px-4 text-right">{registro.leads} Leads</td>
                    <td className="py-3 px-4 text-right font-semibold text-primary-500">
                      {formatCurrency(registro.vendas)}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span className={`font-medium ${registro.roas >= 4 ? 'text-green-500' : 'text-red-500'}`}>
                        {registro.roas?.toFixed(2) || '0.00'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            Nenhum registro encontrado
          </p>
        )}
      </div>
    </div>
  )
}
