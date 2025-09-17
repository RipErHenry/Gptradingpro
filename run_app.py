#!/usr/bin/env python3
"""
GPTading Pro - Launcher Script  
Ejecuta toda la aplicación de trading automatizado
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    try:
        import uvicorn
        import fastapi
        import motor
        print("✅ Backend dependencies OK")
    except ImportError as e:
        print(f"❌ Faltan dependencias del backend: {e}")
        print("💡 Ejecuta: pip install -r backend/requirements.txt")
        return False
    
    # Verificar que Node.js esté disponible
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
        else:
            print("❌ Node.js no encontrado")
            return False
    except FileNotFoundError:
        print("❌ Node.js no está instalado")
        print("💡 Instala Node.js desde: https://nodejs.org/")
        return False
    
    return True

def setup_environment():
    """Configurar variables de entorno"""
    print("⚙️ Configurando entorno...")
    
    # Crear .env para backend si no existe
    backend_env = Path("backend/.env")
    if not backend_env.exists():
        env_content = """MONGO_URL=mongodb://localhost:27017
DB_NAME=gptading_pro"""
        backend_env.write_text(env_content)
        print("✅ Archivo backend/.env creado")
    
    # Crear .env para frontend si no existe  
    frontend_env = Path("frontend/.env")
    if not frontend_env.exists():
        env_content = "REACT_APP_BACKEND_URL=http://localhost:8001"
        frontend_env.write_text(env_content)
        print("✅ Archivo frontend/.env creado")

def install_frontend_deps():
    """Instalar dependencias del frontend"""
    if not Path("frontend/node_modules").exists():
        print("📦 Instalando dependencias del frontend...")
        try:
            subprocess.run(['npm', 'install'], cwd='frontend', check=True)
            print("✅ Dependencias del frontend instaladas")
        except subprocess.CalledProcessError:
            try:
                subprocess.run(['yarn', 'install'], cwd='frontend', check=True)  
                print("✅ Dependencias del frontend instaladas con Yarn")
            except subprocess.CalledProcessError:
                print("❌ Error instalando dependencias del frontend")
                return False
    return True

def run_backend():
    """Ejecutar servidor backend"""
    print("🚀 Iniciando backend...")
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'server:app',
            '--host', '0.0.0.0',
            '--port', '8001',
            '--reload'
        ], cwd='backend')
    except KeyboardInterrupt:
        print("\n🛑 Backend detenido")

def run_frontend():
    """Ejecutar servidor frontend"""
    print("🚀 Iniciando frontend...")  
    try:
        subprocess.run(['npm', 'start'], cwd='frontend')
    except KeyboardInterrupt:
        print("\n🛑 Frontend detenido")
    except FileNotFoundError:
        try:
            subprocess.run(['yarn', 'start'], cwd='frontend')
        except KeyboardInterrupt:
            print("\n🛑 Frontend detenido")

def main():
    """Función principal"""
    print("🎯 GPTading Pro - Launcher")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ Dependencias faltantes. Instala los requisitos primero.")
        return
    
    # Configurar entorno
    setup_environment()
    
    # Instalar dependencias frontend
    if not install_frontend_deps():
        print("❌ Error configurando frontend")
        return
    
    print("\n🎉 ¡Iniciando GPTading Pro!")
    print("📊 Backend API: http://localhost:8001")
    print("🖥️ Frontend: http://localhost:3000") 
    print("📚 Documentación API: http://localhost:8001/docs")
    print("\nPresiona Ctrl+C para detener\n")
    
    # Ejecutar backend y frontend en hilos separados
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    backend_thread.daemon = True
    frontend_thread.daemon = True
    
    backend_thread.start()
    time.sleep(3)  # Dar tiempo al backend para iniciarse
    frontend_thread.start()
    
    try:
        # Mantener el script corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo GPTading Pro...")
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()