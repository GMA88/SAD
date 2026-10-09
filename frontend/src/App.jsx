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
  Activity,
  Plus,
  Trash2,
  RefreshCw,
  Sparkles,
  Search,
  X,
  CheckCircle,
  AlertTriangle,
  DollarSign
} from 'lucide-react'
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts'
import './index.css'

const API_BASE = 'http://127.0.0.1:8000'
const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4', '#ec4899']

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [ventas, setVentas] = useState([])
  const [inventario, setInventario] = useState([])
  const [usuarios, setUsuarios] = useState([])
  const [loading, setLoading] = useState(true)
  const [notification, setNotification] = useState(null)

  // Modales
  const [showProductModal, setShowProductModal] = useState(false)
  const [showSaleModal, setShowSaleModal] = useState(false)
  const [showUserModal, setShowUserModal] = useState(false)
  const [showAiModal, setShowAiModal] = useState(false)
  const [aiReport, setAiReport] = useState(null)
  const [loadingAi, setLoadingAi] = useState(false)

  // Búsqueda y filtros
  const [searchTerm, setSearchTerm] = useState('')

  // Formularios
  const [newProduct, setNewProduct] = useState({
    codigo: '',
    nombre_producto: '',
    cantidad_disponible: 10,
    precio_unitario: 0
  })

  const [newSale, setNewSale] = useState({
    producto_id: '',
    cantidad: 1,
    vendedor: 'Carlos Gómez',
    cliente_nombre: '',
    cliente_contacto: '',
    cliente_telefono: '',
    cliente_email: ''
  })

  const [newUser, setNewUser] = useState({
    username: '',
    password: '',
    role: 'Vendedor'
  })

  const notify = (msg, type = 'success') => {
    setNotification({ msg, type })
    setTimeout(() => setNotification(null), 4000)
  }

  // 1. Cargar datos de la API
  const fetchData = async () => {
    setLoading(true)
    try {
      const [resVentas, resInventario, resUsuarios] = await Promise.all([
        fetch(`${API_BASE}/ventas/`),
        fetch(`${API_BASE}/inventario/`),
        fetch(`${API_BASE}/usuarios/`)
      ])
      
      if (resVentas.ok) setVentas(await resVentas.json())
      if (resInventario.ok) setInventario(await resInventario.json())
      if (resUsuarios.ok) setUsuarios(await resUsuarios.json())
    } catch (error) {
      console.error("Error al conectar con la API:", error)
      notify("Error conectando con la API de FastAPI en el puerto 8000", "error")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  // Cargar datos de demostración
  const handleSeedData = async () => {
    try {
      setLoading(true)
      const res = await fetch(`${API_BASE}/seed`, { method: 'POST' })
      if (res.ok) {
        notify("¡Datos de prueba cargados correctamente!")
        await fetchData()
      } else {
        notify("No se pudieron cargar los datos de prueba", "error")
      }
    } catch (err) {
      notify("Error en la petición de datos demo", "error")
    } finally {
      setLoading(false)
    }
  }

  // Crear producto
  const handleCreateProduct = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_BASE}/inventario/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...newProduct,
          cantidad_disponible: parseInt(newProduct.cantidad_disponible, 10),
          precio_unitario: parseFloat(newProduct.precio_unitario)
        })
      })

      if (res.ok) {
        notify(`Producto "${newProduct.nombre_producto}" creado con éxito`)
        setShowProductModal(false)
        setNewProduct({ codigo: '', nombre_producto: '', cantidad_disponible: 10, precio_unitario: 0 })
        fetchData()
      } else {
        const data = await res.json()
        notify(data.detail || "Error al crear el producto", "error")
      }
    } catch (err) {
      notify("Error de red al crear el producto", "error")
    }
  }

  // Eliminar producto
  const handleDeleteProduct = async (id, nombre) => {
    if (!window.confirm(`¿Estás seguro de eliminar "${nombre}"?`)) return
    try {
      const res = await fetch(`${API_BASE}/inventario/${id}`, { method: 'DELETE' })
      if (res.ok) {
        notify(`Producto "${nombre}" eliminado`)
        fetchData()
      } else {
        notify("No se pudo eliminar el producto", "error")
      }
    } catch (err) {
      notify("Error al eliminar", "error")
    }
  }

  // Registrar Venta
  const handleCreateSale = async (e) => {
    e.preventDefault()
    const prodId = parseInt(newSale.producto_id, 10)
    const selectedProd = inventario.find(p => p.id === prodId)

    if (!selectedProd) {
      notify("Por favor selecciona un producto válido", "error")
      return
    }

    if (newSale.cantidad > selectedProd.cantidad_disponible) {
      notify(`Stock insuficiente. Solo quedan ${selectedProd.cantidad_disponible} unidades disponibles`, "error")
      return
    }

    try {
      const res = await fetch(`${API_BASE}/ventas/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          producto_id: prodId,
          cantidad: parseInt(newSale.cantidad, 10),
          vendedor: newSale.vendedor,
          cliente_nombre: newSale.cliente_nombre,
          cliente_contacto: newSale.cliente_nombre,
          cliente_telefono: newSale.cliente_telefono,
          cliente_email: newSale.cliente_email
        })
      })

      if (res.ok) {
        notify("¡Venta registrada con éxito!")
        setShowSaleModal(false)
        setNewSale({
          producto_id: '',
          cantidad: 1,
          vendedor: 'Carlos Gómez',
          cliente_nombre: '',
          cliente_contacto: '',
          cliente_telefono: '',
          cliente_email: ''
        })
        fetchData()
      } else {
        const data = await res.json()
        notify(data.detail || "Error al procesar la venta", "error")
      }
    } catch (err) {
      notify("Error de red al registrar la venta", "error")
    }
  }

  // Registrar Usuario
  const handleCreateUser = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_BASE}/usuarios/registro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newUser)
      })

      if (res.ok) {
        notify(`Usuario "${newUser.username}" registrado`)
        setShowUserModal(false)
        setNewUser({ username: '', password: '', role: 'Vendedor' })
        fetchData()
      } else {
        const data = await res.json()
        notify(data.detail || "Error al registrar el usuario", "error")
      }
    } catch (err) {
      notify("Error al registrar usuario", "error")
    }
  }

  // Generar Reporte AI
  const handleOpenAiReport = async () => {
    setShowAiModal(true)
    setLoadingAi(true)
    try {
      const res = await fetch(`${API_BASE}/ai/reporte`)
      if (res.ok) {
        setAiReport(await res.json())
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingAi(false)
    }
  }

  // Cálculos de KPIs
  const ingresosTotales = ventas.reduce((acc, v) => acc + (v.total_venta || 0), 0)
  const alertasInventario = inventario.filter(p => p.cantidad_disponible < 5).length
  const ticketPromedio = ventas.length > 0 ? (ingresosTotales / ventas.length).toFixed(2) : 0

  // Gráfica de Ventas cronológica
  const ventasAgrupadas = ventas.slice().sort((a, b) => new Date(a.fecha_venta) - new Date(b.fecha_venta)).reduce((acc, v) => {
    const date = new Date(v.fecha_venta).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
    if (!acc[date]) acc[date] = { name: date, ventas: 0 }
    acc[date].ventas += v.total_venta
    return acc
  }, {})
  
  let salesData = Object.values(ventasAgrupadas)
  if (salesData.length === 0) {
    salesData = [{ name: 'Sin datos', ventas: 0 }]
  }

  // Gráfica de Stock
  const categoryData = inventario.map(p => ({
    name: p.nombre_producto,
    value: p.cantidad_disponible
  }))
  if (categoryData.length === 0) {
    categoryData.push({ name: 'Sin inventario', value: 1 })
  }

  // Productos filtrados para la pestaña de inventario
  const filteredInventory = inventario.filter(p => 
    p.nombre_producto.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.codigo.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const selectedProdObj = inventario.find(p => p.id === parseInt(newSale.producto_id, 10))
  const saleSubtotal = selectedProdObj ? (selectedProdObj.precio_unitario * (newSale.cantidad || 0)).toFixed(2) : 0

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
          <a className={`nav-item ${activeTab === 'inventario' ? 'active' : ''}`} onClick={() => setActiveTab('inventario')}>
            <Package size={20} /> Inventario ({inventario.length})
          </a>
          <a className={`nav-item ${activeTab === 'ventas' ? 'active' : ''}`} onClick={() => setActiveTab('ventas')}>
            <ShoppingCart size={20} /> Ventas ({ventas.length})
          </a>
          <a className={`nav-item ${activeTab === 'usuarios' ? 'active' : ''}`} onClick={() => setActiveTab('usuarios')}>
            <Users size={20} /> Usuarios ({usuarios.length})
          </a>
          
          <div style={{marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid var(--border)'}}>
            <button 
              className="btn btn-secondary" 
              style={{width: '100%', justifyContent: 'center', marginBottom: '10px'}}
              onClick={handleSeedData}
            >
              <RefreshCw size={16} /> Cargar Datos Demo
            </button>
            <div style={{fontSize: '12px', color: 'var(--text-muted)', textAlign: 'center'}}>
              Conectado a FastAPI :8000
            </div>
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Banner de Notificaciones */}
        {notification && (
          <div className={`toast-banner ${notification.type === 'error' ? 'toast-error' : 'toast-success'}`}>
            {notification.type === 'error' ? <AlertTriangle size={18} /> : <CheckCircle size={18} />}
            {notification.msg}
          </div>
        )}

        {/* ================= PESTAÑA: DASHBOARD ================= */}
        {activeTab === 'dashboard' && (
          <>
            <div className="header">
              <div>
                <h1>Dashboard de Inteligencia</h1>
                <p>Métricas empresariales y analítica en tiempo real {loading && "(Actualizando...)"}</p>
              </div>
              <div style={{display: 'flex', gap: '12px'}}>
                <button className="btn btn-secondary" onClick={fetchData} title="Refrescar">
                  <RefreshCw size={16} /> Refrescar
                </button>
                <button className="btn btn-primary" onClick={handleOpenAiReport}>
                  <Sparkles size={16} /> Generar Reporte AI
                </button>
              </div>
            </div>

            {/* KPIs */}
            <div className="dashboard-grid">
              <div className="kpi-card glass-panel">
                <div className="kpi-header">
                  <span className="kpi-title">Ingresos Totales</span>
                  <div className="kpi-icon"><TrendingUp size={24} /></div>
                </div>
                <div className="kpi-value">${ingresosTotales.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</div>
                <div className="kpi-trend trend-up">
                  <ArrowUpRight size={16} /> Acumulado de ventas confirmadas
                </div>
              </div>

              <div className="kpi-card glass-panel">
                <div className="kpi-header">
                  <span className="kpi-title">Ventas Realizadas</span>
                  <div className="kpi-icon"><ShoppingCart size={24} /></div>
                </div>
                <div className="kpi-value">{ventas.length}</div>
                <div className="kpi-trend trend-up">
                  <ArrowUpRight size={16} /> Transacciones registradas en BD
                </div>
              </div>

              <div className="kpi-card glass-panel">
                <div className="kpi-header">
                  <span className="kpi-title">Ticket Promedio</span>
                  <div className="kpi-icon"><DollarSign size={24} /></div>
                </div>
                <div className="kpi-value">${ticketPromedio}</div>
                <div className="kpi-trend trend-up">
                  <ArrowUpRight size={16} /> Promedio por orden
                </div>
              </div>

              <div className="kpi-card glass-panel">
                <div className="kpi-header">
                  <span className="kpi-title">Alertas de Stock</span>
                  <div className="kpi-icon" style={{color: alertasInventario > 0 ? 'var(--warning)' : 'var(--success)'}}>
                    <Activity size={24} />
                  </div>
                </div>
                <div className="kpi-value">{alertasInventario} Prods</div>
                <div className={`kpi-trend ${alertasInventario > 0 ? 'trend-down' : 'trend-up'}`}>
                  {alertasInventario > 0 ? <><ArrowDownRight size={16} /> Menos de 5 unidades</> : <><ArrowUpRight size={16} /> Stock saludable</>}
                </div>
              </div>
            </div>

            {/* Gráficos */}
            <div className="charts-grid">
              <div className="chart-container glass-panel">
                <div className="chart-header">
                  <h2 className="chart-title">Volumen de Ventas en el Tiempo</h2>
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
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }}
                      formatter={(val) => [`$${val}`, 'Ventas']}
                    />
                    <Area type="monotone" dataKey="ventas" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorVentas)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-container glass-panel">
                <div className="chart-header">
                  <h2 className="chart-title">Distribución de Inventario</h2>
                </div>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      innerRadius={65}
                      outerRadius={95}
                      paddingAngle={4}
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
                    <Legend verticalAlign="bottom" height={40} wrapperStyle={{ color: '#94a3b8', fontSize: '12px' }}/>
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}

        {/* ================= PESTAÑA: INVENTARIO ================= */}
        {activeTab === 'inventario' && (
          <div className="glass-panel table-panel">
            <div className="table-toolbar">
              <div>
                <h2>Gestión de Inventario</h2>
                <p style={{color: 'var(--text-muted)', fontSize: '14px'}}>Control de productos, stock disponible y precios unitarios</p>
              </div>
              <div style={{display: 'flex', gap: '12px', alignItems: 'center'}}>
                <div className="search-input-wrapper">
                  <Search size={18} className="search-icon" />
                  <input 
                    type="text" 
                    placeholder="Buscar por nombre o código..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
                <button className="btn btn-primary" onClick={() => setShowProductModal(true)}>
                  <Plus size={16} /> Nuevo Producto
                </button>
              </div>
            </div>

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Código</th>
                    <th>Nombre del Producto</th>
                    <th>Stock</th>
                    <th>Precio Unitario</th>
                    <th>Valor en Inventario</th>
                    <th style={{textAlign: 'right'}}>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredInventory.length === 0 ? (
                    <tr>
                      <td colSpan="6" style={{textAlign: 'center', padding: '32px', color: 'var(--text-muted)'}}>
                        No hay productos registrados en el inventario.
                      </td>
                    </tr>
                  ) : (
                    filteredInventory.map((p) => {
                      const isLow = p.cantidad_disponible < 5
                      const isZero = p.cantidad_disponible === 0
                      return (
                        <tr key={p.id}>
                          <td><strong>{p.codigo}</strong></td>
                          <td>{p.nombre_producto}</td>
                          <td>
                            {isZero ? (
                              <span className="badge badge-danger">Agotado ({p.cantidad_disponible})</span>
                            ) : isLow ? (
                              <span className="badge badge-warning">Stock Bajo ({p.cantidad_disponible})</span>
                            ) : (
                              <span className="badge badge-success">En Stock ({p.cantidad_disponible})</span>
                            )}
                          </td>
                          <td>${p.precio_unitario.toFixed(2)}</td>
                          <td>${(p.cantidad_disponible * p.precio_unitario).toLocaleString('es-MX', { minimumFractionDigits: 2 })}</td>
                          <td style={{textAlign: 'right'}}>
                            <button 
                              className="btn btn-danger btn-icon"
                              title="Eliminar producto"
                              onClick={() => handleDeleteProduct(p.id, p.nombre_producto)}
                            >
                              <Trash2 size={16} />
                            </button>
                          </td>
                        </tr>
                      )
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ================= PESTAÑA: VENTAS ================= */}
        {activeTab === 'ventas' && (
          <div className="glass-panel table-panel">
            <div className="table-toolbar">
              <div>
                <h2>Historial de Ventas</h2>
                <p style={{color: 'var(--text-muted)', fontSize: '14px'}}>Transacciones procesadas en tiempo real con descuento de inventario</p>
              </div>
              <button className="btn btn-primary" onClick={() => setShowSaleModal(true)}>
                <Plus size={16} /> Registrar Venta
              </button>
            </div>

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Fecha</th>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Precio Unit.</th>
                    <th>Total</th>
                    <th>Cliente</th>
                    <th>Vendedor</th>
                  </tr>
                </thead>
                <tbody>
                  {ventas.length === 0 ? (
                    <tr>
                      <td colSpan="8" style={{textAlign: 'center', padding: '32px', color: 'var(--text-muted)'}}>
                        No hay ventas registradas aún. ¡Haz clic en "Registrar Venta" o "Cargar Datos Demo"!
                      </td>
                    </tr>
                  ) : (
                    ventas.map((v) => (
                      <tr key={v.id}>
                        <td>#{v.id}</td>
                        <td>{new Date(v.fecha_venta).toLocaleDateString()} {new Date(v.fecha_venta).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</td>
                        <td><strong>{v.producto?.nombre_producto || `ID Prod: ${v.producto_id}`}</strong></td>
                        <td>{v.cantidad}</td>
                        <td>${v.precio_unitario?.toFixed(2)}</td>
                        <td style={{color: 'var(--success)', fontWeight: 600}}>
                          ${v.total_venta?.toFixed(2)}
                        </td>
                        <td>
                          <div>{v.cliente_nombre}</div>
                          <div style={{fontSize: '12px', color: 'var(--text-muted)'}}>{v.cliente_email}</div>
                        </td>
                        <td><span className="badge badge-info">{v.vendedor}</span></td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ================= PESTAÑA: USUARIOS ================= */}
        {activeTab === 'usuarios' && (
          <div className="glass-panel table-panel">
            <div className="table-toolbar">
              <div>
                <h2>Gestión de Usuarios</h2>
                <p style={{color: 'var(--text-muted)', fontSize: '14px'}}>Usuarios con acceso al sistema y sus roles de autorización</p>
              </div>
              <button className="btn btn-primary" onClick={() => setShowUserModal(true)}>
                <Plus size={16} /> Nuevo Usuario
              </button>
            </div>

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Rol</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {usuarios.length === 0 ? (
                    <tr>
                      <td colSpan="4" style={{textAlign: 'center', padding: '32px', color: 'var(--text-muted)'}}>
                        No hay usuarios cargados.
                      </td>
                    </tr>
                  ) : (
                    usuarios.map((u) => (
                      <tr key={u.id}>
                        <td>#{u.id}</td>
                        <td><strong>{u.username}</strong></td>
                        <td>
                          <span className={`badge ${u.role === 'Administrador' ? 'badge-danger' : u.role === 'Gerente' ? 'badge-warning' : 'badge-info'}`}>
                            {u.role || 'Empleado'}
                          </span>
                        </td>
                        <td>
                          <span className="badge badge-success">Activo</span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* ================= MODAL: NUEVO PRODUCTO ================= */}
      {showProductModal && (
        <div className="modal-overlay" onClick={() => setShowProductModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Registrar Nuevo Producto</h2>
              <button className="close-btn" onClick={() => setShowProductModal(false)}><X size={20} /></button>
            </div>
            <form onSubmit={handleCreateProduct} className="modal-form">
              <div className="form-group">
                <label>Código Único (SKU)</label>
                <input 
                  type="text" 
                  className="form-control" 
                  placeholder="Ej: PRD-009"
                  required
                  value={newProduct.codigo}
                  onChange={(e) => setNewProduct({...newProduct, codigo: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Nombre del Producto</label>
                <input 
                  type="text" 
                  className="form-control" 
                  placeholder="Ej: Teclado Mecánico RGB"
                  required
                  value={newProduct.nombre_producto}
                  onChange={(e) => setNewProduct({...newProduct, nombre_producto: e.target.value})}
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Stock Inicial</label>
                  <input 
                    type="number" 
                    min="0"
                    className="form-control" 
                    required
                    value={newProduct.cantidad_disponible}
                    onChange={(e) => setNewProduct({...newProduct, cantidad_disponible: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Precio Unitario ($)</label>
                  <input 
                    type="number" 
                    step="0.01"
                    min="0"
                    className="form-control" 
                    placeholder="0.00"
                    required
                    value={newProduct.precio_unitario}
                    onChange={(e) => setNewProduct({...newProduct, precio_unitario: e.target.value})}
                  />
                </div>
              </div>
              <div style={{display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '10px'}}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowProductModal(false)}>Cancelar</button>
                <button type="submit" className="btn btn-primary">Guardar Producto</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ================= MODAL: REGISTRAR VENTA ================= */}
      {showSaleModal && (
        <div className="modal-overlay" onClick={() => setShowSaleModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Punto de Venta - Registrar Venta</h2>
              <button className="close-btn" onClick={() => setShowSaleModal(false)}><X size={20} /></button>
            </div>
            <form onSubmit={handleCreateSale} className="modal-form">
              <div className="form-group">
                <label>Selecciona el Producto</label>
                <select 
                  className="form-control"
                  required
                  value={newSale.producto_id}
                  onChange={(e) => setNewSale({...newSale, producto_id: e.target.value})}
                >
                  <option value="">-- Seleccionar Producto --</option>
                  {inventario.map(p => (
                    <option key={p.id} value={p.id} disabled={p.cantidad_disponible <= 0}>
                      {p.nombre_producto} ({p.codigo}) - ${p.precio_unitario} (Stock: {p.cantidad_disponible})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Cantidad</label>
                  <input 
                    type="number" 
                    min="1"
                    max={selectedProdObj ? selectedProdObj.cantidad_disponible : 999}
                    className="form-control" 
                    required
                    value={newSale.cantidad}
                    onChange={(e) => setNewSale({...newSale, cantidad: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Total Calculado</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    readOnly
                    value={`$${saleSubtotal} USD`}
                    style={{background: 'rgba(59, 130, 246, 0.1)', color: 'var(--accent)', fontWeight: 'bold'}}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Nombre del Cliente / Empresa</label>
                <input 
                  type="text" 
                  className="form-control" 
                  placeholder="Ej: Banco Corporativo"
                  required
                  value={newSale.cliente_nombre}
                  onChange={(e) => setNewSale({...newSale, cliente_nombre: e.target.value})}
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Email de Contacto</label>
                  <input 
                    type="email" 
                    className="form-control" 
                    placeholder="cliente@ejemplo.com"
                    required
                    value={newSale.cliente_email}
                    onChange={(e) => setNewSale({...newSale, cliente_email: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Teléfono</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    placeholder="+52 55 ..."
                    required
                    value={newSale.cliente_telefono}
                    onChange={(e) => setNewSale({...newSale, cliente_telefono: e.target.value})}
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Vendedor Responsable</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={newSale.vendedor}
                  onChange={(e) => setNewSale({...newSale, vendedor: e.target.value})}
                />
              </div>

              <div style={{display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '10px'}}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowSaleModal(false)}>Cancelar</button>
                <button type="submit" className="btn btn-primary">Confirmar Venta</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ================= MODAL: NUEVO USUARIO ================= */}
      {showUserModal && (
        <div className="modal-overlay" onClick={() => setShowUserModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Crear Usuario del Sistema</h2>
              <button className="close-btn" onClick={() => setShowUserModal(false)}><X size={20} /></button>
            </div>
            <form onSubmit={handleCreateUser} className="modal-form">
              <div className="form-group">
                <label>Nombre de Usuario</label>
                <input 
                  type="text" 
                  className="form-control" 
                  required
                  placeholder="Ej: sofia_admin"
                  value={newUser.username}
                  onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Contraseña</label>
                <input 
                  type="password" 
                  className="form-control" 
                  required
                  placeholder="••••••••"
                  value={newUser.password}
                  onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Rol de Acceso</label>
                <select 
                  className="form-control"
                  value={newUser.role}
                  onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                >
                  <option value="Administrador">Administrador</option>
                  <option value="Gerente">Gerente</option>
                  <option value="Vendedor">Vendedor</option>
                </select>
              </div>
              <div style={{display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '10px'}}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowUserModal(false)}>Cancelar</button>
                <button type="submit" className="btn btn-primary">Registrar Usuario</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ================= MODAL: REPORTE AI ================= */}
      {showAiModal && (
        <div className="modal-overlay" onClick={() => setShowAiModal(false)}>
          <div className="modal-content" style={{maxWidth: '650px'}} onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
                <Sparkles size={24} style={{color: 'var(--accent)'}} />
                <h2>Reporte Ejecutivo con Inteligencia Artificial</h2>
              </div>
              <button className="close-btn" onClick={() => setShowAiModal(false)}><X size={20} /></button>
            </div>

            {loadingAi ? (
              <div style={{textAlign: 'center', padding: '40px', color: 'var(--text-muted)'}}>
                <RefreshCw size={32} className="spin" style={{margin: '0 auto 16px', display: 'block'}} />
                Analizando métricas de ventas, stock y patrones de demanda...
              </div>
            ) : aiReport ? (
              <div style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
                <div className="glass-panel" style={{padding: '16px', background: 'rgba(59, 130, 246, 0.1)', borderColor: 'rgba(59, 130, 246, 0.3)'}}>
                  <div style={{fontWeight: 600, color: 'var(--accent)', marginBottom: '6px'}}>Diagnóstico General</div>
                  <div style={{fontSize: '14px', lineHeight: '1.6'}}>{aiReport.resumen_ejecutivo}</div>
                </div>

                <div>
                  <div style={{fontWeight: 600, color: '#f59e0b', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px'}}>
                    <AlertTriangle size={16} /> Alertas Críticas
                  </div>
                  <ul style={{paddingLeft: '20px', fontSize: '13px', display: 'flex', flexDirection: 'column', gap: '6px'}}>
                    {aiReport.alertas_criticas.map((alerta, i) => (
                      <li key={i} style={{color: '#f87171'}}>{alerta}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <div style={{fontWeight: 600, color: '#10b981', marginBottom: '8px'}}>Recomendaciones Estratégicas</div>
                  <ul style={{paddingLeft: '20px', fontSize: '13px', display: 'flex', flexDirection: 'column', gap: '6px'}}>
                    {aiReport.recomendaciones.map((rec, i) => (
                      <li key={i} style={{color: 'var(--text-muted)'}}>{rec}</li>
                    ))}
                  </ul>
                </div>

                <div style={{background: 'rgba(16, 185, 129, 0.1)', padding: '12px 16px', borderRadius: '10px', border: '1px solid rgba(16, 185, 129, 0.3)', fontSize: '13px', color: '#34d399'}}>
                  <strong>Proyección:</strong> {aiReport.proyeccion_crecimiento}
                </div>

                <div style={{display: 'flex', justifyContent: 'flex-end', marginTop: '10px'}}>
                  <button className="btn btn-secondary" onClick={() => setShowAiModal(false)}>Cerrar</button>
                </div>
              </div>
            ) : (
              <div>No se pudo generar el reporte.</div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
