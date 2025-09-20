#!/usr/bin/env python3
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
