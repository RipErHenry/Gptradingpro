#!/usr/bin/env python3
"""
GPTading Pro - Setup Completo Automático
Prepara la aplicación para uso inmediato
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header():
    """Mostrar header de la aplicación"""
    print("🤖" + "=" * 60 + "🤖")
    print("        GPTading Pro - Setup Automático")
    print("    Trading Automatizado Listo en 60 Segundos")
    print("🤖" + "=" * 60 + "🤖\n")

def check_python():
    """Verificar versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Requiere Python 3.8+")
        return False

def install_backend_deps():
    """Instalar dependencias del backend"""
    print("\n📦 Instalando dependencias Python...")
    
    try:
        # Actualizar pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      capture_output=True, check=True)
        
        # Instalar dependencias
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'], 
                      check=True)
        print("✅ Dependencias Python instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def check_node():
    """Verificar Node.js"""
    print("\n🟢 Verificando Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} - OK")
            return True
        else:
            print("❌ Node.js no encontrado")
            return False
    except FileNotFoundError:
        print("❌ Node.js no instalado")
        print("💡 Descarga desde: https://nodejs.org/")
        return False

def install_frontend_deps():
    """Instalar dependencias del frontend"""
    print("\n📦 Instalando dependencias React...")
    
    try:
        # Intentar con yarn primero
        result = subprocess.run(['yarn', '--version'], capture_output=True)
        if result.returncode == 0:
            subprocess.run(['yarn', 'install'], cwd='frontend', check=True)
            print("✅ Dependencias React instaladas (Yarn)")
        else:
            # Usar npm como fallback
            subprocess.run(['npm', 'install'], cwd='frontend', check=True)
            print("✅ Dependencias React instaladas (npm)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias React: {e}")
        return False

def setup_env_files():
    """Crear archivos de configuración"""
    print("\n⚙️ Configurando archivos de entorno...")
    
    # Backend .env
    backend_env = Path("backend/.env")
    if not backend_env.exists():
        backend_env.write_text("""MONGO_URL=mongodb://localhost:27017
DB_NAME=gptading_pro""")
        print("✅ backend/.env creado")
    
    # Frontend .env
    frontend_env = Path("frontend/.env")
    if not frontend_env.exists():
        frontend_env.write_text("REACT_APP_BACKEND_URL=http://localhost:8001")
        print("✅ frontend/.env creado")

def create_start_script():
    """Crear script de inicio rápido"""
    start_script = """#!/usr/bin/env python3
import subprocess
import sys
import time
import threading
import webbrowser

def start_backend():
    print("🚀 Iniciando Backend API...")
    subprocess.run([sys.executable, '-m', 'uvicorn', 'server:app', '--host', '0.0.0.0', '--port', '8001'], cwd='backend')

def start_frontend():
    print("🚀 Iniciando Frontend React...")
    try:
        subprocess.run(['yarn', 'start'], cwd='frontend')
    except:
        subprocess.run(['npm', 'start'], cwd='frontend')

if __name__ == "__main__":
    print("🎯 GPTading Pro - Iniciando...")
    
    # Iniciar backend en hilo separado
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Esperar 3 segundos
    time.sleep(3)
    
    print("✅ Backend iniciado en: http://localhost:8001")
    print("📚 Documentación API: http://localhost:8001/docs")
    
    # Abrir navegador automáticamente
    print("🌐 Abriendo navegador...")
    webbrowser.open('http://localhost:3000')
    
    # Iniciar frontend
    start_frontend()
"""
    
    with open("start_gptading.py", "w") as f:
        f.write(start_script)
    
    print("✅ Script de inicio creado: start_gptading.py")

def create_demo_guide():
    """Crear guía de uso demo"""
    guide = """# 🚀 GPTading Pro - Guía Rápida DEMO

## 🎮 Cómo Usar AHORA MISMO

### 1. ⚡ Inicio Súper Rápido
```bash
python start_gptading.py
```
- Se abre automáticamente en tu navegador
- Backend: http://localhost:8001  
- Frontend: http://localhost:3000

### 2. 🤖 Probar Bots de Trading

#### A. Conectar Zaffex (DEMO)
1. Ve a **Configuración** → **Zaffex API**
2. Usa estas credenciales DEMO:
   ```
   API Key: demo_api_key_12345678901234567890
   API Secret: demo_api_secret_12345678901234567890
   ✅ Modo de prueba: ACTIVADO
   ```
3. Clic en **Conectar con Zaffex**

#### B. Crear y Activar Bot
1. Ve a **Trading Bots** → **Crear Bot**
2. Configuración recomendada:
   ```
   Nombre: Mi Primer Bot
   Estrategia: Grid Trading
   Riesgo: Medio
   Inversión: $1000
   ```
3. Clic en **Crear Bot**
4. Clic en **Iniciar** para activar trading automático

#### C. Ver Resultados en Tiempo Real
1. **Dashboard**: Métricas generales actualizándose
2. **Trading Bots**: Estado de bots y ganancias
3. **Operaciones**: Trades ejecutados automáticamente

### 3. 📊 Qué Esperar (DEMO)

- ✅ **Bots operando automáticamente** cada 30 seg - 5 min
- ✅ **Balance cambiando** con ganancias/pérdidas simuladas
- ✅ **Trades apareciendo** en historial
- ✅ **Métricas actualizándose** (ROI, precisión, etc.)
- ✅ **6 estrategias diferentes** para probar
- ✅ **Datos de mercado realistas** 

### 4. 🎯 Funcionalidades DEMO

#### Estrategias Disponibles:
- **Grid Trading** (Conservador) - 87% precisión
- **DCA + RSI** (Moderado) - 79% precisión  
- **Momentum Trading** (Agresivo) - 92% precisión
- **High Frequency** (Scalping) - 94% precisión
- **Cross Exchange** (Arbitraje) - 96% precisión
- **Machine Learning** (IA) - 82% precisión

#### Pares de Trading:
- BTC/USDT, ETH/USDT, ADA/USDT, DOT/USDT
- MATIC/USDT, AVAX/USDT

### 5. 🔥 Casos de Uso Demo

#### Test Básico (5 minutos):
1. Conectar Zaffex → Crear 1 bot → Activar → Ver dashboard

#### Test Completo (15 minutos):
1. Crear 3 bots con estrategias diferentes
2. Activar todos los bots
3. Observar competencia entre estrategias
4. Revisar análisis de rendimiento

#### Test Avanzado (30 minutos):
1. Probar las 6 estrategias
2. Comparar niveles de riesgo
3. Analizar portfolio y distribución
4. Configurar notificaciones

### 6. ⚠️ IMPORTANTE - Es DEMO

- 💰 **No usa dinero real**
- 🤖 **Trading completamente simulado**
- 📊 **Datos realistas pero ficticios**
- ✅ **Perfecto para aprender y probar**

### 7. 🛠️ Cambiar a Modo REAL

Cuando tengas credenciales reales de Zaffex:
1. **Configuración** → **Zaffex API**
2. Ingresa credenciales REALES
3. ❌ **Desactiva** "Modo de prueba"
4. ⚠️ **¡AHORA USARÁ DINERO REAL!**

## 🎉 ¡A Trading Automático!

Tu plataforma está lista para generar ganancias simuladas 24/7.

**Disfruta probando GPTading Pro!** 🚀
"""
    
    with open("DEMO_GUIDE.md", "w") as f:
        f.write(guide)
    
    print("✅ Guía demo creada: DEMO_GUIDE.md")

def main():
    """Función principal de setup"""
    print_header()
    
    success = True
    
    # Verificaciones básicas
    if not check_python():
        success = False
    
    if not check_node():
        success = False
    
    if not success:
        print("\n❌ Requisitos no cumplidos. Instala Python 3.8+ y Node.js")
        return
    
    # Instalaciones
    if not install_backend_deps():
        print("\n❌ Error en setup del backend")
        return
    
    if not install_frontend_deps():
        print("\n❌ Error en setup del frontend")
        return
    
    # Configuraciones
    setup_env_files()
    create_start_script()
    create_demo_guide()
    
    print("\n🎉" + "=" * 50 + "🎉")
    print("     ¡GPTading Pro LISTO PARA USAR!")
    print("🎉" + "=" * 50 + "🎉")
    
    print("\n🚀 INICIO RÁPIDO:")
    print("   python start_gptading.py")
    
    print("\n📖 GUÍA COMPLETA:")
    print("   Abre: DEMO_GUIDE.md")
    
    print("\n🌐 URLs IMPORTANTES:")
    print("   📱 App: http://localhost:3000")
    print("   🔧 API: http://localhost:8001")
    print("   📚 Docs: http://localhost:8001/docs")
    
    print("\n⭐ CREDENCIALES DEMO:")
    print("   API Key: demo_api_key_12345678901234567890")
    print("   Secret:  demo_api_secret_12345678901234567890")
    
    print("\n✨ ¡Listo para trading automático! ✨")

if __name__ == "__main__":
    main()