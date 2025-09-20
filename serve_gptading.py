#!/usr/bin/env python3
"""
GPTading Pro - Servidor Web Simple
Ejecuta la aplicación sin mostrar index.html en la URL
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os
from pathlib import Path

class GPTadingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def do_GET(self):
        # Si acceden a la raíz, servir index.html automáticamente
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        
        # Agregar headers CORS para desarrollo
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        return super().do_GET()

def open_browser(url, delay=2):
    """Abrir navegador después de un delay"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"🌐 Navegador abierto: {url}")
    except Exception as e:
        print(f"❌ No se pudo abrir el navegador automáticamente: {e}")
        print(f"📌 Abre manualmente: {url}")

def start_server():
    """Iniciar servidor GPTading Pro"""
    PORT = 8080
    
    print("🚀 GPTading Pro - Servidor Web")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), GPTadingHandler) as httpd:
            server_url = f"http://localhost:{PORT}"
            
            print(f"✅ Servidor iniciado en: {server_url}")
            print(f"📱 GPTading Pro disponible en: {server_url}")
            print(f"🛑 Para detener: Ctrl+C")
            print("=" * 50)
            
            # Abrir navegador en hilo separado
            browser_thread = threading.Thread(target=open_browser, args=(server_url,))
            browser_thread.daemon = True
            browser_thread.start()
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Puerto {PORT} ya está en uso")
            print("💡 Intenta con otro puerto o cierra otras aplicaciones")
        else:
            print(f"❌ Error al iniciar servidor: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
        print("👋 ¡GPTading Pro cerrado!")

if __name__ == "__main__":
    start_server()