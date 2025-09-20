# 🚀 GPTading Pro - Trading Automatizado Inteligente

<div align="center">

![GPTading Pro](https://img.shields.io/badge/GPTading-Pro-blue?style=for-the-badge&logo=bitcoin)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-19.0-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green?style=for-the-badge&logo=mongodb)

**Plataforma Completa de Trading Automatizado con IA**
*Conecta con Zaffex Broker • Operaciones 24/7 • Máxima Rentabilidad*

[🎮 Demo en Vivo](#-demo-rápido) • [📚 Documentación](#-documentación) • [🚀 Deployment](#-deployment-producción) • [💰 Trading Real](#-trading-real)

</div>

---

## 🎯 **Descripción del Proyecto**

GPTading Pro es una plataforma revolucionaria de **trading automatizado** que utiliza **inteligencia artificial** para ejecutar operaciones de criptomonedas de forma autónoma. Conecta directamente con **Zaffex Broker** para realizar operaciones reales con diferentes estrategias de riesgo optimizadas.

### 🏆 **Características Destacadas**

| Característica | Descripción |
|----------------|-------------|
| 🤖 **6 Estrategias IA** | Grid Trading, DCA+RSI, Momentum, HFT, Arbitraje, Machine Learning |
| ⚡ **Trading 24/7** | Operaciones automáticas sin intervención humana |
| 🎯 **3 Niveles Riesgo** | Conservador, Moderado, Agresivo |
| 🔗 **Zaffex Integration** | Conexión real con broker para operaciones en vivo |
| 📊 **Dashboard Real-time** | Métricas, gráficos y análisis en tiempo real |
| 🛡️ **Gestión de Riesgo** | Stop-loss, take-profit, límites configurables |

---

## 🚀 **Inicio Rápido (3 minutos)**

### **Opción A: Ejecución Ultra Rápida**
```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/gptading-pro.git
cd gptading-pro

# 2. Setup automático
python setup_gptading.py

# 3. ¡Lanzar aplicación!
python start_gptading.py
```

### **Opción B: Deployment Docker (Producción)**
```bash
# Deployment completo en un comando
./deploy.sh

# URLs disponibles:
# Frontend: http://localhost:3000
# Backend:  http://localhost:8001
# API Docs: http://localhost:8001/docs
```

---

## 🎮 **Demo Rápido**

### **🟢 Modo Demo (Sin Riesgo)**
```bash
# Credenciales demo incluidas:
API Key:    demo_api_key_12345678901234567890
API Secret: demo_api_secret_12345678901234567890
Modo:       ✅ Prueba (Datos simulados)
```

### **🔴 Trading Real (Dinero Real)**
```bash
# Configurar con credenciales reales de Zaffex:
API Key:    [Tu clave real de Zaffex]
API Secret: [Tu secreto real de Zaffex] 
Modo:       ❌ Producción (¡DINERO REAL!)
```

---

## 📊 **Tecnologías & Arquitectura**

### **Stack Tecnológico**
```
Frontend:   React 19 + Tailwind CSS + Shadcn/UI
Backend:    Python + FastAPI + AsyncIO
Database:   MongoDB + Motor (Async)
Broker:     Zaffex Integration (Real Trading)
Deploy:     Docker + Docker Compose + Nginx
```

### **Arquitectura del Sistema**
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   React     │    │   FastAPI    │    │  MongoDB    │
│  Frontend   │◄──►│   Backend    │◄──►│  Database   │
└─────────────┘    └──────────────┘    └─────────────┘
                           │
                   ┌──────────────┐
                   │    Zaffex    │
                   │   Broker     │
                   └──────────────┘
```

---

## 🤖 **Estrategias de Trading IA**

| Estrategia | Descripción | Riesgo | ROI Esperado |
|------------|-------------|---------|--------------|
| **Grid Trading** | Órdenes automáticas en rangos | 🟢 Bajo | 8-15% |
| **DCA + RSI** | Promedio de costo + análisis técnico | 🟡 Medio | 12-25% |
| **Momentum** | Seguimiento de tendencias fuertes | 🔴 Alto | 20-50% |
| **High Frequency** | Scalping ultrarrápido | 🟡 Medio | 15-30% |
| **Cross Exchange** | Arbitraje entre exchanges | 🟢 Bajo | 5-12% |
| **Machine Learning** | Predicciones con IA avanzada | 🔴 Alto | 25-60% |

---

## 📱 **Capturas de Pantalla**

### Dashboard Principal
![Dashboard](https://via.placeholder.com/800x400/1a1a1a/00d4ff?text=Dashboard+GPTading+Pro)

### Gestión de Bots
![Bots](https://via.placeholder.com/800x400/1a1a1a/00ff88?text=Trading+Bots+Management)

### Configuración Zaffex
![Settings](https://via.placeholder.com/800x400/1a1a1a/ff6b00?text=Zaffex+Integration)

---

## 🔧 **Configuración Detallada**

### **Requisitos del Sistema**
```bash
Python:     3.8+
Node.js:    16+
MongoDB:    4.4+
RAM:        4GB mínimo
Storage:    10GB disponible
```

### **Variables de Entorno**
```env
# Backend (.env)
MONGO_URL=mongodb://localhost:27017
DB_NAME=gptading_pro
JWT_SECRET_KEY=your-secret-key

# Frontend (.env)
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 🚀 **Deployment Producción**

### **Docker Compose (Recomendado)**
```bash
# Configuración completa lista para producción
docker-compose -f docker-compose.prod.yml up -d

# Incluye:
# - MongoDB con persistencia
# - Backend con múltiples workers
# - Frontend con Nginx optimizado
# - SSL/HTTPS configurado
# - Backup automático
```

### **Hosting Manual**
```bash
# 1. Setup servidor
./QUICK_SETUP.sh

# 2. Configurar dominio
# Editar: frontend/.env.production

# 3. Deploy
./deploy.sh

# 4. Monitoreo
./health_check.sh
```

---

## 💰 **Trading Real**

### **⚠️ Advertencias Importantes**
- **RIESGO REAL**: Los bots usan dinero verdadero
- **EMPEZAR PEQUEÑO**: Probar con $10-50 inicialmente  
- **MONITOREO**: Supervisar constantemente las primeras horas
- **STOP-LOSS**: Configurar límites de pérdida siempre

### **Configuración Segura**
```bash
# 1. Obtener API Keys en Zaffex.com
# 2. Restricciones de IP recomendadas
# 3. Permisos mínimos (solo trading, sin withdraw)
# 4. Empezar en modo testnet
```

---

## 📚 **Documentación**

| Documento | Descripción |
|-----------|-------------|
| [📋 contracts.md](contracts.md) | Contratos API completos |
| [🚀 PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) | Guía de producción |
| [🎮 DEMO_GUIDE.md](DEMO_GUIDE.md) | Guía de demo rápida |
| [🔧 API Docs](http://localhost:8001/docs) | Documentación interactiva |

---

## 🛠️ **Desarrollo**

### **Estructura del Proyecto**
```
gptading-pro/
├── 📁 frontend/              # React App
│   ├── src/components/       # Componentes UI
│   ├── src/pages/           # Páginas principales
│   └── src/utils/           # Utilidades y API
├── 📁 backend/              # FastAPI Server  
│   ├── models/              # Modelos de datos
│   ├── routes/              # Endpoints API
│   ├── services/            # Servicios (Zaffex, etc.)
│   └── server.py            # Servidor principal
├── 🐳 docker-compose.prod.yml  # Docker producción
├── 🚀 deploy.sh             # Script deployment
└── 📚 README.md             # Este archivo
```

### **API Endpoints Principales**
```
GET    /api/health           # Health check
GET    /api/bots             # Listar bots
POST   /api/bots             # Crear bot
POST   /api/bots/{id}/activate  # Activar bot
GET    /api/portfolio        # Portfolio info
POST   /api/zaffex/connect   # Conectar Zaffex
```

---

## 🤝 **Contribución**

### **Cómo Contribuir**
1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-estrategia`)
3. Commit cambios (`git commit -m 'Add: Nueva estrategia ML'`)
4. Push rama (`git push origin feature/nueva-estrategia`)
5. Abrir Pull Request

### **Agregar Nueva Estrategia**
```python
# 1. Editar backend/models/bot.py
class Strategy(str, Enum):
    NUEVA_ESTRATEGIA = "Nueva Estrategia"

# 2. Implementar lógica en backend/routes/bots.py
# 3. Actualizar frontend/src/utils/mockData.js
# 4. Testing y documentación
```

---

## 🆘 **Soporte y Troubleshooting**

### **Problemas Comunes**
| Problema | Solución |
|----------|----------|
| Backend no inicia | Verificar MongoDB + `pip install -r requirements.txt` |
| Frontend error | Verificar Node.js + `npm install` |
| Zaffex no conecta | Verificar credenciales + modo test |
| Bots no operan | Verificar balance + conexión Zaffex |

### **Logs y Debugging**
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Health check completo
./health_check.sh

# Backend logs específicos
tail -f /var/log/gptading/backend.log
```

---

## 📄 **Licencia**

```
MIT License - Uso libre para proyectos personales y comerciales
Ver archivo LICENSE para detalles completos
```

---

## 🎉 **¡Únete a la Revolución del Trading Automatizado!**

<div align="center">

### **🚀 ¡Empieza Ahora Mismo!**

```bash
git clone https://github.com/tu-usuario/gptading-pro.git && cd gptading-pro && python start_gptading.py
```

**[⭐ Star este repo](https://github.com/tu-usuario/gptading-pro)** • **[🐛 Reportar bug](https://github.com/tu-usuario/gptading-pro/issues)** • **[💡 Sugerir feature](https://github.com/tu-usuario/gptading-pro/issues)**

---

*Desarrollado con ❤️ para la comunidad de trading automatizado*

**GPTading Pro** - *Where AI Meets Profit* 🚀💰

</div>