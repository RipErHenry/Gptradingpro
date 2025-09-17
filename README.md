# 🤖 GPTading Pro - Trading Automatizado Inteligente

Una plataforma completa de trading automatizado que se conecta con Zaffex broker para ejecutar operaciones de criptomonedas usando bots inteligentes con diferentes estrategias de riesgo.

## 🎯 Características Principales

### 🤖 **Bots de Trading Automatizado**
- **6 Estrategias Diferentes**: Grid Trading, DCA + RSI, Momentum, High Frequency, Arbitraje, Machine Learning
- **3 Niveles de Riesgo**: Conservador, Moderado, Agresivo  
- **Trading 24/7**: Operaciones automáticas sin intervención manual
- **Gestión de Riesgo**: Stop-loss y take-profit configurables

### 📊 **Dashboard Avanzado**
- Métricas de rendimiento en tiempo real
- Portfolio tracking completo
- Historial de operaciones detallado
- Análisis de precisión por estrategia

### 🔗 **Integración Zaffex Broker**
- Conexión segura con API keys
- Balance y datos de mercado en tiempo real
- Ejecución automática de órdenes
- Historial de operaciones sincronizado

## 🚀 Instalación y Uso

### **Opción 1: Ejecución Automática (Recomendada)**
```bash
# 1. Instalar dependencias Python
pip install -r backend/requirements.txt

# 2. Ejecutar aplicación completa
python run_app.py
```

### **Opción 2: Ejecución Manual**
```bash
# Terminal 1 - Backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend  
cd frontend
npm install && npm start
```

### **Acceso a la Aplicación**
- 🖥️ **Frontend**: http://localhost:3000
- 🔧 **API Backend**: http://localhost:8001
- 📚 **Documentación**: http://localhost:8001/docs

## 📦 Crear Paquete para Distribución

```bash
# Comprimir aplicación completa
python package_app.py

# Resultado: gptading_pro_YYYYMMDD_HHMMSS.zip
```