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

// Datos de prueba (Mock Data) para visualización
const salesData = [
  { name: 'Ene', ventas: 4000, costo: 2400 },
  { name: 'Feb', ventas: 3000, costo: 1398 },
  { name: 'Mar', ventas: 5000, costo: 3800 },
  { name: 'Abr', ventas: 2780, costo: 1908 },
  { name: 'May', ventas: 6890, costo: 4800 },
  { name: 'Jun', ventas: 8390, costo: 3800 },
  { name: 'Jul', ventas: 10490, costo: 4300 },
]

const categoryData = [
  { name: 'Electrónicos', value: 400 },
  { name: 'Ropa', value: 300 },
  { name: 'Alimentos', value: 300 },
  { name: 'Hogar', value: 200 },
]

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

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
            <p>Resumen de rendimiento y métricas clave de negocio</p>
          </div>
          <button className="glass-panel" style={{padding: '12px 24px', color: '#fff', border: '1px solid var(--accent)', background: 'var(--accent)', cursor: 'pointer'}}>
            Generar Reporte AI
          </button>
        </div>

        {/* KPIs */}
        <div className="dashboard-grid">
          <div className="kpi-card glass-panel">
            <div className="kpi-header">
              <span className="kpi-title">Ingresos Totales</span>
              <div className="kpi-icon"><TrendingUp size={24} /></div>
            </div>
            <div className="kpi-value">$42,500</div>
            <div className="kpi-trend trend-up">
              <ArrowUpRight size={16} /> +12.5% desde el mes pasado
            </div>
          </div>

          <div className="kpi-card glass-panel">
            <div className="kpi-header">
              <span className="kpi-title">Ventas Realizadas</span>
              <div className="kpi-icon"><ShoppingCart size={24} /></div>
            </div>
            <div className="kpi-value">1,204</div>
            <div className="kpi-trend trend-up">
              <ArrowUpRight size={16} /> +5.2% desde el mes pasado
            </div>
          </div>

          <div className="kpi-card glass-panel">
            <div className="kpi-header">
              <span className="kpi-title">Alertas de Inventario</span>
              <div className="kpi-icon" style={{color: 'var(--warning)', background: 'rgba(245, 158, 11, 0.1)'}}>
                <Activity size={24} />
              </div>
            </div>
            <div className="kpi-value">12 Prods</div>
            <div className="kpi-trend trend-down">
              <ArrowDownRight size={16} /> Requieren reabastecimiento
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="charts-grid">
          <div className="chart-container glass-panel">
            <div className="chart-header">
              <h2 className="chart-title">Análisis de Ingresos vs Costos</h2>
            </div>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={salesData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorVentas" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorCosto" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
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
                <Area type="monotone" dataKey="costo" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorCosto)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container glass-panel">
            <div className="chart-header">
              <h2 className="chart-title">Distribución de Ventas</h2>
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
