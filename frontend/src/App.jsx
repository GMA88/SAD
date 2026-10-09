import React, { useState, useEffect } from 'react'
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  Users,
  Settings,
  TrendingUp,
  ArrowUpRight,
  ArrowDownRight,
  Activity
} from 'lucide-react'
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Legend, PieChart, Pie, Cell
} from 'recharts'
import './index.css'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444']

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [ventas, setVentas] = useState([])
  const [inventario, setInventario] = useState([])
  const [loading, setLoading] = useState(true)

  // 1. Cargar datos desde FastAPI
  useEffect(() => {
    const fetchData = async () => {
      try {
        const resVentas = await fetch('http://127.0.0.1:8000/ventas/')
        const resInventario = await fetch('http://127.0.0.1:8000/inventario/')
        
        if (resVentas.ok) setVentas(await resVentas.json())
        if (resInventario.ok) setInventario(await resInventario.json())
      } catch (error) {
        console.error("Error de conexión con la API:", error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])

  // 2. Calcular KPIs reales basados en los datos
  const ingresosTotales = ventas.reduce((acc, v) => acc + (v.total_venta || 0), 0)
  const alertasInventario = inventario.filter(p => p.cantidad_disponible < 5).length
  
  // 3. Preparar datos reales para las gráficas
  // Agrupar ventas por fecha
  const ventasAgrupadas = ventas.reduce((acc, v) => {
    const date = new Date(v.fecha_venta).toLocaleDateString()
    if (!acc[date]) acc[date] = { name: date, ventas: 0 }
    acc[date].ventas += v.total_venta
    return acc
  }, {})
  
  let salesData = Object.values(ventasAgrupadas)
  if (salesData.length === 0) {
    salesData = [{ name: 'Sin datos', ventas: 0 }] // Fallback si la BD está vacía
  }

  // Agrupar inventario para ver qué producto tiene más stock
  const categoryData = inventario.slice(0, 5).map(p => ({
    name: p.nombre_producto,
    value: p.cantidad_disponible
  }))
  
  if (categoryData.length === 0) {
    categoryData.push({ name: 'Vacío', value: 1 })
  }

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar glass-panel">
        <div className="logo">
          <div className="logo-icon">▲</div>
          SAD ERP
        </div>
        
        <nav className="nav-menu">
          <a className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <LayoutDashboard size={20} /> Dashboard
          </a>
          <a className={`nav-item ${activeTab === 'ventas' ? 'active' : ''}`} onClick={() => setActiveTab('ventas')}>
            <ShoppingCart size={20} /> Ventas
          </a>
          <a className={`nav-item ${activeTab === 'inventario' ? 'active' : ''}`} onClick={() => setActiveTab('inventario')}>
            <Package size={20} /> Inventario
          </a>
          <a className={`nav-item ${activeTab === 'usuarios' ? 'active' : ''}`} onClick={() => setActiveTab('usuarios')}>
            <Users size={20} /> Usuarios
          </a>
          <a className="nav-item" style={{marginTop: 'auto'}}>
            <Settings size={20} /> Configuración
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="header">
          <div>
            <h1>Dashboard de Inteligencia</h1>
            <p>Conectado a FastAPI en tiempo real {loading && "(Cargando...)"}</p>
          </div>
          <button className="glass-panel" style={{padding: '12px 24px', color: '#fff', border: '1px solid var(--accent)', background: 'var(--accent)', cursor: 'pointer'}}>
            Generar Reporte AI
          </button>
        </div>

        {/* KPIs Reales */}
        <div className="dashboard-grid">
          <div className="kpi-card glass-panel">
            <div className="kpi-header">
              <span className="kpi-title">Ingresos Totales</span>
              <div className="kpi-icon"><TrendingUp size={24} /></div>
            </div>
            <div className="kpi-value">${ingresosTotales.toLocaleString()}</div>
            <div className="kpi-trend trend-up">
              <ArrowUpRight size={16} /> Dinero generado históricamente
            </div>
          </div>

          <div className="kpi-card glass-panel">
            <div className="kpi-header">
              <span className="kpi-title">Ventas Realizadas</span>
              <div className="kpi-icon"><ShoppingCart size={24} /></div>
            </div>
            <div className="kpi-value">{ventas.length}</div>
            <div className="kpi-trend trend-up">
              <ArrowUpRight size={16} /> Transacciones registradas
            </div>
          </div>

          <div className="kpi-card glass-panel">
            <div className="kpi-header">
              <span className="kpi-title">Alertas de Inventario</span>
              <div className="kpi-icon" style={{color: alertasInventario > 0 ? 'var(--warning)' : 'var(--success)', background: 'rgba(245, 158, 11, 0.1)'}}>
                <Activity size={24} />
              </div>
            </div>
            <div className="kpi-value">{alertasInventario} Prods</div>
            <div className={`kpi-trend ${alertasInventario > 0 ? 'trend-down' : 'trend-up'}`}>
              {alertasInventario > 0 ? <><ArrowDownRight size={16} /> Con menos de 5 unidades</> : <><ArrowUpRight size={16} /> Stock saludable</>}
            </div>
          </div>
        </div>

        {/* Charts Reales */}
        <div className="charts-grid">
          <div className="chart-container glass-panel">
            <div className="chart-header">
              <h2 className="chart-title">Análisis de Ingresos por Día</h2>
            </div>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={salesData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorVentas" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="ventas" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorVentas)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container glass-panel">
            <div className="chart-header">
              <h2 className="chart-title">Stock por Producto</h2>
            </div>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={110}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                />
                <Legend verticalAlign="bottom" height={36} wrapperStyle={{ color: '#94a3b8' }}/>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

      </main>
    </div>
  )
}

export default App
