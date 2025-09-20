#!/usr/bin/env python3
"""
GPTading Pro - Deploy Online Automático
Sube la aplicación a hosting gratuito sin index.html visible
"""

import os
import json
import subprocess
from pathlib import Path

def create_netlify_config():
    """Crear configuración para Netlify"""
    
    netlify_config = """# Netlify Configuration for GPTading Pro
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    
[[headers]]
  for = "*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000"

[[headers]]
  for = "*.css"  
  [headers.values]
    Cache-Control = "public, max-age=31536000"
"""
    
    with open("netlify.toml", "w") as f:
        f.write(netlify_config)
    
    print("✅ netlify.toml creado")

def create_vercel_config():
    """Crear configuración para Vercel"""
    
    vercel_config = {
        "version": 2,
        "name": "gptading-pro",
        "builds": [
            {
                "src": "index.html",
                "use": "@vercel/static"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/index.html"
            }
        ],
        "headers": [
            {
                "source": "/(.*)",
                "headers": [
                    {
                        "key": "X-Frame-Options",
                        "value": "DENY"
                    },
                    {
                        "key": "X-Content-Type-Options", 
                        "value": "nosniff"
                    }
                ]
            }
        ]
    }
    
    with open("vercel.json", "w") as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ vercel.json creado")

def create_surge_config():
    """Crear configuración para Surge.sh"""
    
    # CNAME para dominio personalizado (opcional)
    surge_cname = "gptading-pro.surge.sh"
    
    with open("CNAME", "w") as f:
        f.write(surge_cname)
    
    print("✅ CNAME creado para Surge.sh")

def create_firebase_config():
    """Crear configuración para Firebase Hosting"""
    
    firebase_config = {
        "hosting": {
            "public": ".",
            "ignore": [
                "firebase.json",
                "**/.*",
                "**/node_modules/**"
            ],
            "rewrites": [
                {
                    "source": "**",
                    "destination": "/index.html"
                }
            ],
            "headers": [
                {
                    "source": "**/*.@(js|css)",
                    "headers": [
                        {
                            "key": "Cache-Control",
                            "value": "max-age=31536000"
                        }
                    ]
                }
            ]
        }
    }
    
    with open("firebase.json", "w") as f:
        json.dump(firebase_config, f, indent=2)
    
    print("✅ firebase.json creado")

def show_deployment_instructions():
    """Mostrar instrucciones de deployment"""
    
    print("\n🚀 GPTading Pro - Instrucciones de Deploy")
    print("=" * 60)
    
    print("\n🌐 NETLIFY (Más fácil - Drag & Drop):")
    print("1. Ve a: https://netlify.com")
    print("2. Arrastra toda la carpeta al área de drop")
    print("3. ¡Listo! URL: https://random-name.netlify.app")
    
    print("\n⚡ VERCEL (GitHub integration):")
    print("1. Ve a: https://vercel.com") 
    print("2. Conecta con GitHub")
    print("3. Import repository")
    print("4. Deploy automático")
    
    print("\n🔥 SURGE.SH (Línea de comandos):")
    print("1. npm install -g surge")
    print("2. surge")
    print("3. Seguir instrucciones")
    print("4. URL: https://gptading-pro.surge.sh")
    
    print("\n🚀 FIREBASE HOSTING:")
    print("1. npm install -g firebase-tools")
    print("2. firebase login")
    print("3. firebase init hosting")
    print("4. firebase deploy")
    
    print("\n✅ RESULTADO:")
    print("- URL limpia sin index.html")
    print("- HTTPS automático") 
    print("- CDN global incluido")
    print("- Hosting gratuito")

def main():
    """Función principal"""
    print("🌐 GPTading Pro - Preparando para Deploy Online")
    print("=" * 60)
    
    # Crear configuraciones para diferentes plataformas
    create_netlify_config()
    create_vercel_config() 
    create_surge_config()
    create_firebase_config()
    
    # Mostrar instrucciones
    show_deployment_instructions()
    
    print(f"\n📁 Archivos creados en: {Path.cwd()}")
    print("🎯 Elige tu plataforma favorita y sigue las instrucciones")

if __name__ == "__main__":
    main()