# API del Sistema de Soporte - Guía Frontend

## Descripción General
Esta documentación cubre la integración frontend del sistema de soporte completo, incluyendo tickets, chat en tiempo real, FAQ y gestión de casos de soporte.

## Autenticación
```javascript
const token = localStorage.getItem('authToken');
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

## 1. GESTIÓN DE TICKETS

### 1.1 Crear Ticket
```javascript
const crearTicket = async (datosTicket) => {
  try {
    const response = await fetch('http://localhost:8000/api/soporte/tickets/', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        asunto: datosTicket.asunto,
        categoria: datosTicket.categoria, // TECNICO, RESERVAS, PAGOS, GENERAL
        prioridad: datosTicket.prioridad, // ALTA, MEDIA, BAJA
        descripcion: datosTicket.descripcion,
        archivos_adjuntos: datosTicket.archivos || [],
        reserva_relacionada: datosTicket.reservaId || null
      })
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const ticket = await response.json();
    return ticket;
  } catch (error) {
    console.error('Error al crear ticket:', error);
    throw error;
  }
};

// Uso
const nuevoTicket = {
  asunto: "Problema con el pago de mi reserva",
  categoria: "PAGOS",
  prioridad: "ALTA",
  descripcion: "No puedo completar el pago de mi reserva #123",
  reservaId: 123
};

crearTicket(nuevoTicket);
```

### 1.2 Obtener Tickets del Usuario
```javascript
const obtenerMisTickets = async (filtros = {}) => {
  try {
    const params = new URLSearchParams({
      page: filtros.page || 1,
      size: filtros.size || 10,
      estado: filtros.estado || '', // ABIERTO, EN_PROGRESO, RESUELTO, CERRADO
      categoria: filtros.categoria || '',
      fecha_desde: filtros.fechaDesde || '',
      fecha_hasta: filtros.fechaHasta || ''
    });
    
    const response = await fetch(`http://localhost:8000/api/soporte/mis-tickets/?${params}`, {
      method: 'GET',
      headers: headers
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error al obtener tickets:', error);
    throw error;
  }
};

// Componente React para lista de tickets
const ListaTickets = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtros, setFiltros] = useState({});

  useEffect(() => {
    const cargarTickets = async () => {
      setLoading(true);
      try {
        const data = await obtenerMisTickets(filtros);
        setTickets(data.results);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    cargarTickets();
  }, [filtros]);

  return (
    <div className="tickets-container">
      <div className="tickets-filters">
        <select 
          value={filtros.estado || ''} 
          onChange={(e) => setFiltros({...filtros, estado: e.target.value})}
        >
          <option value="">Todos los estados</option>
          <option value="ABIERTO">Abierto</option>
          <option value="EN_PROGRESO">En Progreso</option>
          <option value="RESUELTO">Resuelto</option>
          <option value="CERRADO">Cerrado</option>
        </select>
        
        <select 
          value={filtros.categoria || ''} 
          onChange={(e) => setFiltros({...filtros, categoria: e.target.value})}
        >
          <option value="">Todas las categorías</option>
          <option value="TECNICO">Técnico</option>
          <option value="RESERVAS">Reservas</option>
          <option value="PAGOS">Pagos</option>
          <option value="GENERAL">General</option>
        </select>
      </div>

      {loading ? (
        <div className="loading">Cargando tickets...</div>
      ) : (
        <div className="tickets-list">
          {tickets.map(ticket => (
            <div key={ticket.id} className="ticket-card">
              <div className="ticket-header">
                <h3>#{ticket.numero} - {ticket.asunto}</h3>
                <span className={`estado ${ticket.estado.toLowerCase()}`}>
                  {ticket.estado}
                </span>
              </div>
              <div className="ticket-meta">
                <span>Categoría: {ticket.categoria}</span>
                <span>Prioridad: {ticket.prioridad}</span>
                <span>Creado: {new Date(ticket.fecha_creacion).toLocaleDateString()}</span>
              </div>
              <p className="ticket-descripcion">{ticket.descripcion}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

### 1.3 Obtener Detalle de Ticket
```javascript
const obtenerDetalleTicket = async (ticketId) => {
  try {
    const response = await fetch(`http://localhost:8000/api/soporte/tickets/${ticketId}/`, {
      method: 'GET',
      headers: headers
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const ticket = await response.json();
    return ticket;
  } catch (error) {
    console.error('Error al obtener detalle del ticket:', error);
    throw error;
  }
};

// Componente React para detalle de ticket
const DetalleTicket = ({ ticketId }) => {
  const [ticket, setTicket] = useState(null);
  const [respuestas, setRespuestas] = useState([]);
  const [nuevaRespuesta, setNuevaRespuesta] = useState('');

  useEffect(() => {
    const cargarTicket = async () => {
      try {
        const ticketData = await obtenerDetalleTicket(ticketId);
        setTicket(ticketData);
        setRespuestas(ticketData.respuestas || []);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    cargarTicket();
  }, [ticketId]);

  if (!ticket) return <div>Cargando...</div>;

  return (
    <div className="ticket-detalle">
      <div className="ticket-header">
        <h2>#{ticket.numero} - {ticket.asunto}</h2>
        <div className="ticket-status">
          <span className={`estado ${ticket.estado.toLowerCase()}`}>
            {ticket.estado}
          </span>
          <span className={`prioridad ${ticket.prioridad.toLowerCase()}`}>
            {ticket.prioridad}
          </span>
        </div>
      </div>

      <div className="ticket-info">
        <p><strong>Categoría:</strong> {ticket.categoria}</p>
        <p><strong>Fecha de creación:</strong> {new Date(ticket.fecha_creacion).toLocaleString()}</p>
        <p><strong>Última actualización:</strong> {new Date(ticket.fecha_actualizacion).toLocaleString()}</p>
        {ticket.reserva_relacionada && (
          <p><strong>Reserva relacionada:</strong> #{ticket.reserva_relacionada.id}</p>
        )}
      </div>

      <div className="ticket-descripcion">
        <h3>Descripción</h3>
        <p>{ticket.descripcion}</p>
      </div>

      {ticket.archivos_adjuntos && ticket.archivos_adjuntos.length > 0 && (
        <div className="ticket-archivos">
          <h3>Archivos adjuntos</h3>
          {ticket.archivos_adjuntos.map((archivo, index) => (
            <a key={index} href={archivo.url} target="_blank" rel="noopener noreferrer">
              {archivo.nombre}
            </a>
          ))}
        </div>
      )}

      <div className="ticket-respuestas">
        <h3>Conversación</h3>
        {respuestas.map(respuesta => (
          <div key={respuesta.id} className="respuesta">
            <div className="respuesta-header">
              <strong>{respuesta.autor.nombre}</strong>
              <span className="fecha">{new Date(respuesta.fecha_creacion).toLocaleString()}</span>
            </div>
            <p>{respuesta.mensaje}</p>
            {respuesta.archivos_adjuntos && respuesta.archivos_adjuntos.length > 0 && (
              <div className="respuesta-archivos">
                {respuesta.archivos_adjuntos.map((archivo, index) => (
                  <a key={index} href={archivo.url} target="_blank" rel="noopener noreferrer">
                    {archivo.nombre}
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 1.4 Responder a Ticket
```javascript
const responderTicket = async (ticketId, mensaje, archivos = []) => {
  try {
    const formData = new FormData();
    formData.append('mensaje', mensaje);
    
    archivos.forEach((archivo, index) => {
      formData.append(`archivo_${index}`, archivo);
    });
    
    const response = await fetch(`http://localhost:8000/api/soporte/tickets/${ticketId}/responder/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const respuesta = await response.json();
    return respuesta;
  } catch (error) {
    console.error('Error al responder ticket:', error);
    throw error;
  }
};

// Componente para responder tickets
const ResponderTicket = ({ ticketId, onRespuestaEnviada }) => {
  const [mensaje, setMensaje] = useState('');
  const [archivos, setArchivos] = useState([]);
  const [enviando, setEnviando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    setEnviando(true);
    try {
      await responderTicket(ticketId, mensaje, archivos);
      setMensaje('');
      setArchivos([]);
      onRespuestaEnviada();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setEnviando(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="responder-ticket">
      <div className="form-group">
        <label>Respuesta:</label>
        <textarea
          value={mensaje}
          onChange={(e) => setMensaje(e.target.value)}
          placeholder="Escribe tu respuesta..."
          rows={4}
          required
        />
      </div>

      <div className="form-group">
        <label>Archivos adjuntos:</label>
        <input
          type="file"
          multiple
          onChange={(e) => setArchivos(Array.from(e.target.files))}
        />
      </div>

      <button type="submit" disabled={enviando || !mensaje.trim()}>
        {enviando ? 'Enviando...' : 'Enviar Respuesta'}
      </button>
    </form>
  );
};
```

## 2. CHAT EN TIEMPO REAL

### 2.1 Conexión WebSocket
```javascript
class ChatSoporteWebSocket {
  constructor(ticketId, onMessage) {
    this.ticketId = ticketId;
    this.onMessage = onMessage;
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    const token = localStorage.getItem('authToken');
    const wsUrl = `ws://localhost:8000/ws/soporte/ticket/${this.ticketId}/?token=${token}`;
    
    this.socket = new WebSocket(wsUrl);
    
    this.socket.onopen = () => {
      console.log('Chat WebSocket conectado');
      this.reconnectAttempts = 0;
    };
    
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.onMessage(data);
    };
    
    this.socket.onclose = (event) => {
      console.log('Chat WebSocket desconectado');
      if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          this.reconnectAttempts++;
          this.connect();
        }, this.reconnectDelay * this.reconnectAttempts);
      }
    };
    
    this.socket.onerror = (error) => {
      console.error('Error en WebSocket:', error);
    };
  }

  sendMessage(mensaje, tipo = 'mensaje') {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({
        tipo: tipo,
        mensaje: mensaje,
        timestamp: new Date().toISOString()
      }));
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close(1000);
    }
  }
}

// Hook para usar el chat WebSocket
const useChatSoporte = (ticketId) => {
  const [mensajes, setMensajes] = useState([]);
  const [conectado, setConectado] = useState(false);
  const chatRef = useRef(null);

  useEffect(() => {
    const handleMessage = (data) => {
      switch (data.tipo) {
        case 'mensaje':
          setMensajes(prev => [...prev, data]);
          break;
        case 'typing':
          // Manejar indicador de escritura
          break;
        case 'connection_status':
          setConectado(data.conectado);
          break;
      }
    };

    chatRef.current = new ChatSoporteWebSocket(ticketId, handleMessage);
    chatRef.current.connect();

    return () => {
      if (chatRef.current) {
        chatRef.current.disconnect();
      }
    };
  }, [ticketId]);

  const enviarMensaje = (mensaje) => {
    if (chatRef.current) {
      chatRef.current.sendMessage(mensaje);
    }
  };

  return { mensajes, conectado, enviarMensaje };
};
```

### 2.2 Componente Chat en Tiempo Real
```javascript
const ChatTicket = ({ ticketId }) => {
  const { mensajes, conectado, enviarMensaje } = useChatSoporte(ticketId);
  const [nuevoMensaje, setNuevoMensaje] = useState('');
  const [escribiendo, setEscribiendo] = useState(false);
  const mensajesRef = useRef(null);

  useEffect(() => {
    // Scroll automático al último mensaje
    if (mensajesRef.current) {
      mensajesRef.current.scrollTop = mensajesRef.current.scrollHeight;
    }
  }, [mensajes]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!nuevoMensaje.trim() || !conectado) return;

    enviarMensaje(nuevoMensaje);
    setNuevoMensaje('');
  };

  const handleTyping = useCallback(
    debounce(() => setEscribiendo(false), 1000),
    []
  );

  const handleInputChange = (e) => {
    setNuevoMensaje(e.target.value);
    if (!escribiendo) {
      setEscribiendo(true);
      // Enviar indicador de escritura
    }
    handleTyping();
  };

  return (
    <div className="chat-ticket">
      <div className="chat-header">
        <h3>Chat en Tiempo Real</h3>
        <div className="chat-status">
          <span className={`status ${conectado ? 'conectado' : 'desconectado'}`}>
            {conectado ? 'Conectado' : 'Desconectado'}
          </span>
        </div>
      </div>

      <div className="chat-mensajes" ref={mensajesRef}>
        {mensajes.map((mensaje, index) => (
          <div key={index} className={`mensaje ${mensaje.tipo}`}>
            <div className="mensaje-header">
              <strong>{mensaje.autor}</strong>
              <span className="timestamp">
                {new Date(mensaje.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <p>{mensaje.contenido}</p>
          </div>
        ))}
        {escribiendo && (
          <div className="typing-indicator">
            <span>Agente está escribiendo...</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={nuevoMensaje}
          onChange={handleInputChange}
          placeholder="Escribe tu mensaje..."
          disabled={!conectado}
        />
        <button type="submit" disabled={!conectado || !nuevoMensaje.trim()}>
          Enviar
        </button>
      </form>
    </div>
  );
};
```

## 3. SISTEMA FAQ

### 3.1 Obtener FAQs
```javascript
const obtenerFAQs = async (categoria = '', busqueda = '') => {
  try {
    const params = new URLSearchParams({
      categoria: categoria,
      q: busqueda,
      activas: 'true'
    });
    
    const response = await fetch(`http://localhost:8000/api/soporte/faqs/?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const faqs = await response.json();
    return faqs;
  } catch (error) {
    console.error('Error al obtener FAQs:', error);
    throw error;
  }
};

// Componente FAQ
const FAQ = () => {
  const [faqs, setFaqs] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState('');
  const [busqueda, setBusqueda] = useState('');
  const [expandido, setExpandido] = useState({});

  useEffect(() => {
    const cargarFAQs = async () => {
      try {
        const data = await obtenerFAQs(categoriaSeleccionada, busqueda);
        setFaqs(data.results || data);
        
        // Extraer categorías únicas
        const cats = [...new Set(data.results?.map(faq => faq.categoria) || [])];
        setCategorias(cats);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    cargarFAQs();
  }, [categoriaSeleccionada, busqueda]);

  const toggleExpandido = (faqId) => {
    setExpandido(prev => ({
      ...prev,
      [faqId]: !prev[faqId]
    }));
  };

  return (
    <div className="faq-container">
      <div className="faq-header">
        <h2>Preguntas Frecuentes</h2>
        
        <div className="faq-filters">
          <input
            type="text"
            placeholder="Buscar en FAQs..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="faq-search"
          />
          
          <select
            value={categoriaSeleccionada}
            onChange={(e) => setCategoriaSeleccionada(e.target.value)}
            className="faq-category-filter"
          >
            <option value="">Todas las categorías</option>
            {categorias.map(categoria => (
              <option key={categoria} value={categoria}>
                {categoria}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="faq-list">
        {faqs.map(faq => (
          <div key={faq.id} className="faq-item">
            <div 
              className="faq-pregunta"
              onClick={() => toggleExpandido(faq.id)}
            >
              <h3>{faq.pregunta}</h3>
              <span className={`faq-toggle ${expandido[faq.id] ? 'expanded' : ''}`}>
                ▼
              </span>
            </div>
            
            {expandido[faq.id] && (
              <div className="faq-respuesta">
                <p>{faq.respuesta}</p>
                <div className="faq-meta">
                  <span>Categoría: {faq.categoria}</span>
                  <span>Útil: {faq.valoraciones_positivas} ✓ / {faq.valoraciones_negativas} ✗</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 3.2 Valorar FAQ
```javascript
const valorarFAQ = async (faqId, esUtil) => {
  try {
    const response = await fetch(`http://localhost:8000/api/soporte/faqs/${faqId}/valorar/`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        es_util: esUtil
      })
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const resultado = await response.json();
    return resultado;
  } catch (error) {
    console.error('Error al valorar FAQ:', error);
    throw error;
  }
};
```

## 4. GESTIÓN DE CASOS DE SOPORTE

### 4.1 Crear Caso de Soporte
```javascript
const crearCasoSoporte = async (datosCaso) => {
  try {
    const response = await fetch('http://localhost:8000/api/soporte/casos/', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        tipo_caso: datosCaso.tipo, // RECLAMO, SUGERENCIA, CONSULTA, INCIDENTE
        urgencia: datosCaso.urgencia, // CRITICA, ALTA, MEDIA, BAJA
        titulo: datosCaso.titulo,
        descripcion: datosCaso.descripcion,
        cliente_afectado: datosCaso.clienteId,
        reservas_relacionadas: datosCaso.reservasIds || [],
        impacto_estimado: datosCaso.impacto || 'INDIVIDUAL'
      })
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const caso = await response.json();
    return caso;
  } catch (error) {
    console.error('Error al crear caso:', error);
    throw error;
  }
};

// Formulario de creación de caso
const FormularioCaso = ({ onCasoCreado }) => {
  const [caso, setCaso] = useState({
    tipo: 'CONSULTA',
    urgencia: 'MEDIA',
    titulo: '',
    descripcion: '',
    impacto: 'INDIVIDUAL'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const nuevoCaso = await crearCasoSoporte(caso);
      onCasoCreado(nuevoCaso);
      setCaso({
        tipo: 'CONSULTA',
        urgencia: 'MEDIA',
        titulo: '',
        descripcion: '',
        impacto: 'INDIVIDUAL'
      });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="formulario-caso">
      <div className="form-group">
        <label>Tipo de Caso:</label>
        <select
          value={caso.tipo}
          onChange={(e) => setCaso({...caso, tipo: e.target.value})}
          required
        >
          <option value="CONSULTA">Consulta</option>
          <option value="RECLAMO">Reclamo</option>
          <option value="SUGERENCIA">Sugerencia</option>
          <option value="INCIDENTE">Incidente</option>
        </select>
      </div>

      <div className="form-group">
        <label>Urgencia:</label>
        <select
          value={caso.urgencia}
          onChange={(e) => setCaso({...caso, urgencia: e.target.value})}
          required
        >
          <option value="BAJA">Baja</option>
          <option value="MEDIA">Media</option>
          <option value="ALTA">Alta</option>
          <option value="CRITICA">Crítica</option>
        </select>
      </div>

      <div className="form-group">
        <label>Título:</label>
        <input
          type="text"
          value={caso.titulo}
          onChange={(e) => setCaso({...caso, titulo: e.target.value})}
          required
        />
      </div>

      <div className="form-group">
        <label>Descripción:</label>
        <textarea
          value={caso.descripcion}
          onChange={(e) => setCaso({...caso, descripcion: e.target.value})}
          rows={4}
          required
        />
      </div>

      <button type="submit">Crear Caso</button>
    </form>
  );
};
```

### 4.2 Dashboard de Soporte
```javascript
const DashboardSoporte = () => {
  const [estadisticas, setEstadisticas] = useState(null);
  const [ticketsRecientes, setTicketsRecientes] = useState([]);
  const [casosUrgentes, setCasosUrgentes] = useState([]);

  useEffect(() => {
    const cargarDashboard = async () => {
      try {
        // Cargar estadísticas
        const statsResponse = await fetch('http://localhost:8000/api/soporte/dashboard/stats/', {
          headers: headers
        });
        const stats = await statsResponse.json();
        setEstadisticas(stats);

        // Cargar tickets recientes
        const ticketsResponse = await fetch('http://localhost:8000/api/soporte/tickets/recientes/', {
          headers: headers
        });
        const tickets = await ticketsResponse.json();
        setTicketsRecientes(tickets);

        // Cargar casos urgentes
        const casosResponse = await fetch('http://localhost:8000/api/soporte/casos/urgentes/', {
          headers: headers
        });
        const casos = await casosResponse.json();
        setCasosUrgentes(casos);
      } catch (error) {
        console.error('Error al cargar dashboard:', error);
      }
    };

    cargarDashboard();
  }, []);

  if (!estadisticas) return <div>Cargando dashboard...</div>;

  return (
    <div className="dashboard-soporte">
      <h2>Dashboard de Soporte</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Tickets Abiertos</h3>
          <div className="stat-number">{estadisticas.tickets_abiertos}</div>
        </div>
        
        <div className="stat-card">
          <h3>Tiempo Promedio Respuesta</h3>
          <div className="stat-number">{estadisticas.tiempo_promedio_respuesta}h</div>
        </div>
        
        <div className="stat-card">
          <h3>Satisfacción</h3>
          <div className="stat-number">{estadisticas.satisfaccion_promedio}%</div>
        </div>
        
        <div className="stat-card">
          <h3>Casos Críticos</h3>
          <div className="stat-number">{estadisticas.casos_criticos}</div>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="tickets-recientes">
          <h3>Tickets Recientes</h3>
          {ticketsRecientes.map(ticket => (
            <div key={ticket.id} className="ticket-item">
              <span>#{ticket.numero}</span>
              <span>{ticket.asunto}</span>
              <span className={`estado ${ticket.estado.toLowerCase()}`}>
                {ticket.estado}
              </span>
            </div>
          ))}
        </div>

        <div className="casos-urgentes">
          <h3>Casos Urgentes</h3>
          {casosUrgentes.map(caso => (
            <div key={caso.id} className="caso-item">
              <span>{caso.titulo}</span>
              <span className={`urgencia ${caso.urgencia.toLowerCase()}`}>
                {caso.urgencia}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

## 5. ESCALAMIENTO AUTOMÁTICO

### 5.1 Configurar Reglas de Escalamiento
```javascript
const configurarEscalamiento = async (reglas) => {
  try {
    const response = await fetch('http://localhost:8000/api/soporte/escalamiento/reglas/', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        tiempo_respuesta_maximo: reglas.tiempoMaximo, // en horas
        prioridades_escalamiento: reglas.prioridades, // array de prioridades
        niveles_escalamiento: reglas.niveles, // niveles de escalamiento
        notificaciones_automaticas: reglas.notificaciones
      })
    });
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    const resultado = await response.json();
    return resultado;
  } catch (error) {
    console.error('Error al configurar escalamiento:', error);
    throw error;
  }
};
```

### 5.2 Monitor de Escalamiento
```javascript
const MonitorEscalamiento = () => {
  const [ticketsEscalados, setTicketsEscalados] = useState([]);
  const [alertas, setAlertas] = useState([]);

  useEffect(() => {
    const cargarEscalamiento = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/soporte/escalamiento/monitor/', {
          headers: headers
        });
        const data = await response.json();
        
        setTicketsEscalados(data.tickets_escalados);
        setAlertas(data.alertas);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    cargarEscalamiento();
    
    // Actualizar cada 30 segundos
    const interval = setInterval(cargarEscalamiento, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="monitor-escalamiento">
      <h3>Monitor de Escalamiento</h3>
      
      {alertas.length > 0 && (
        <div className="alertas">
          <h4>Alertas Activas</h4>
          {alertas.map(alerta => (
            <div key={alerta.id} className={`alerta ${alerta.nivel}`}>
              <span>{alerta.mensaje}</span>
              <span>{new Date(alerta.timestamp).toLocaleString()}</span>
            </div>
          ))}
        </div>
      )}

      <div className="tickets-escalados">
        <h4>Tickets Escalados</h4>
        {ticketsEscalados.map(ticket => (
          <div key={ticket.id} className="ticket-escalado">
            <span>#{ticket.numero}</span>
            <span>{ticket.asunto}</span>
            <span>Escalado hace: {ticket.tiempo_escalamiento}</span>
            <span>Nivel: {ticket.nivel_escalamiento}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

## 6. INTEGRACIÓN COMPLETA

### 6.1 Proveedor de Contexto de Soporte
```javascript
const SoporteContext = createContext();

export const SoporteProvider = ({ children }) => {
  const [ticketsActivos, setTicketsActivos] = useState([]);
  const [chatActivo, setChatActivo] = useState(null);
  const [notificacionesSoporte, setNotificacionesSoporte] = useState([]);

  const crearTicketRapido = async (datos) => {
    try {
      const nuevoTicket = await crearTicket(datos);
      setTicketsActivos(prev => [nuevoTicket, ...prev]);
      return nuevoTicket;
    } catch (error) {
      throw error;
    }
  };

  const iniciarChat = (ticketId) => {
    setChatActivo(ticketId);
  };

  const cerrarChat = () => {
    setChatActivo(null);
  };

  return (
    <SoporteContext.Provider value={{
      ticketsActivos,
      setTicketsActivos,
      chatActivo,
      iniciarChat,
      cerrarChat,
      crearTicketRapido,
      notificacionesSoporte,
      setNotificacionesSoporte
    }}>
      {children}
    </SoporteContext.Provider>
  );
};

export const useSoporte = () => {
  const context = useContext(SoporteContext);
  if (!context) {
    throw new Error('useSoporte debe usarse dentro de SoporteProvider');
  }
  return context;
};
```

### 6.2 Widget de Soporte Flotante
```javascript
const WidgetSoporte = () => {
  const [abierto, setAbierto] = useState(false);
  const [vista, setVista] = useState('menu'); // menu, faq, ticket, chat
  const { ticketsActivos, crearTicketRapido } = useSoporte();

  const opcionesMenu = [
    { id: 'faq', label: 'Preguntas Frecuentes', icono: '❓' },
    { id: 'ticket', label: 'Crear Ticket', icono: '🎫' },
    { id: 'chat', label: 'Chat en Vivo', icono: '💬' },
    { id: 'mis-tickets', label: 'Mis Tickets', icono: '📋' }
  ];

  return (
    <div className={`widget-soporte ${abierto ? 'abierto' : ''}`}>
      <button 
        className="widget-toggle"
        onClick={() => setAbierto(!abierto)}
      >
        {abierto ? '✕' : '❓'}
      </button>

      {abierto && (
        <div className="widget-contenido">
          <div className="widget-header">
            <h3>¿Necesitas Ayuda?</h3>
            {vista !== 'menu' && (
              <button onClick={() => setVista('menu')}>← Volver</button>
            )}
          </div>

          <div className="widget-body">
            {vista === 'menu' && (
              <div className="menu-opciones">
                {opcionesMenu.map(opcion => (
                  <button
                    key={opcion.id}
                    className="opcion-menu"
                    onClick={() => setVista(opcion.id)}
                  >
                    <span className="icono">{opcion.icono}</span>
                    <span className="label">{opcion.label}</span>
                  </button>
                ))}
              </div>
            )}

            {vista === 'faq' && <FAQ />}
            {vista === 'ticket' && <FormularioTicketRapido />}
            {vista === 'chat' && <ChatSoporteRapido />}
            {vista === 'mis-tickets' && <MisTicketsWidget />}
          </div>
        </div>
      )}
    </div>
  );
};
```

Esta documentación proporciona una integración completa del sistema de soporte, incluyendo tickets, chat en tiempo real, FAQ, casos de soporte y escalamiento automático. Todos los componentes están diseñados para trabajar juntos y ofrecer una experiencia de soporte integral para los usuarios.