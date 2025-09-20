#!/usr/bin/env python3
"""
GPTading Pro - Production Package Creator
Crea paquete completo listo para hosting real
"""

import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

def create_production_package():
    """Crear paquete completo de producción"""
    
    print("🚀 Creando GPTading Pro - Paquete de Producción")
    print("=" * 60)
    
    # Nombre del paquete
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"gptading_pro_production_{timestamp}.zip"
    
    print(f"📦 Archivo de salida: {package_name}")
    
    # Archivos y directorios a incluir
    production_files = [
        # Aplicación principal
        "frontend/",
        "backend/",
        
        # Configuraciones de producción
        "docker-compose.prod.yml",
        "deploy.sh",
        "backup.sh", 
        "health_check.sh",
        
        # Scripts de setup
        "setup_gptading.py",
        "start_gptading.py",
        "deploy_production.py",
        "create_production_package.py",
        
        # Documentación
        "README.md",
        "PRODUCTION_GUIDE.md",
        "DEMO_GUIDE.md",
        "contracts.md"
    ]
    
    # Archivos a excluir
    exclude_patterns = [
        "__pycache__",
        "node_modules",
        ".git",
        "*.pyc",
        "*.log",
        ".DS_Store",
        "build/",
        "dist/",
        ".env.local",
        "npm-debug.log*",
        "yarn-debug.log*",
        "yarn-error.log*"
    ]
    
    print("📁 Empaquetando archivos...")
    
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        
        # Agregar README principal
        readme_content = create_main_readme()
        zipf.writestr("README_PRODUCTION.md", readme_content)
        
        # Agregar script de setup rápido
        quick_setup = create_quick_setup_script()
        zipf.writestr("QUICK_SETUP.sh", quick_setup)
        
        base_dir = Path(".")
        
        for include_item in production_files:
            include_path = base_dir / include_item
            
            if include_path.is_file():
                zipf.write(include_path, include_item)
                print(f"✅ Agregado archivo: {include_item}")
                
            elif include_path.is_dir():
                files_added = 0
                for root, dirs, files in os.walk(include_path):
                    # Filtrar directorios excluidos
                    dirs[:] = [d for d in dirs if not should_exclude(d, exclude_patterns)]
                    
                    for file in files:
                        if should_exclude(file, exclude_patterns):
                            continue
                            
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(base_dir)
                        zipf.write(file_path, arc_name)
                        files_added += 1
                
                print(f"✅ Agregado directorio: {include_item} ({files_added} archivos)")
        
        # Agregar archivos de configuración adicionales
        add_production_configs(zipf)
    
    # Información del paquete
    package_size = os.path.getsize(package_name) / (1024 * 1024)
    
    print("\n🎉" + "=" * 50 + "🎉")
    print("   ¡PAQUETE DE PRODUCCIÓN CREADO!")
    print("🎉" + "=" * 50 + "🎉")
    
    print(f"\n📦 ARCHIVO: {package_name}")
    print(f"📏 TAMAÑO: {package_size:.1f} MB")
    
    print("\n🚀 INSTRUCCIONES DE USO:")
    print("1. Descomprimir en servidor de producción")
    print("2. Ejecutar: chmod +x QUICK_SETUP.sh && ./QUICK_SETUP.sh")
    print("3. Configurar dominio en archivos .env")
    print("4. Ejecutar: ./deploy.sh")
    
    print("\n📋 CONTENIDO DEL PAQUETE:")
    print("✅ Aplicación React completa")
    print("✅ Backend FastAPI con Zaffex real") 
    print("✅ Configuración Docker para producción")
    print("✅ Scripts de deployment automático")
    print("✅ Configuración SSL/HTTPS")
    print("✅ Sistema de backup y monitoreo")
    print("✅ Documentación completa")
    
    print("\n🌐 URLS DE PRODUCCIÓN:")
    print("📱 Frontend: https://tudominio.com")
    print("🔧 API: https://tudominio.com/api")
    print("📚 Docs: https://tudominio.com/api/docs")
    
    print(f"\n✨ ¡Listo para hosting real! ✨")
    
    return package_name

def should_exclude(name, patterns):
    """Verificar si un archivo/directorio debe ser excluido"""
    for pattern in patterns:
        if pattern in name or name.startswith('.'):
            return True
    return False

def create_main_readme():
    """Crear README principal para producción"""
    return """# 🚀 GPTading Pro - Producción

## 🎯 Deployment Ultra Rápido

### ⚡ Instalación en 3 Comandos
```bash
# 1. Descomprimir
unzip gptading_pro_production_*.zip
cd gptading-pro

# 2. Setup automático  
chmod +x QUICK_SETUP.sh && ./QUICK_SETUP.sh

# 3. Desplegar
./deploy.sh
```

## 🌐 URLs de Acceso
- **Frontend**: https://tudominio.com
- **API**: https://tudominio.com/api  
- **Documentación**: https://tudominio.com/api/docs

## 🔧 Configuración Mínima Requerida

### Servidor
- Ubuntu 20.04+ / CentOS 8+
- 2 CPU cores, 4GB RAM, 20GB SSD
- Docker y Docker Compose instalados

### Dominio y DNS
- Dominio apuntando a IP del servidor
- Certificado SSL (Let's Encrypt incluido)

## 📋 Archivos Importantes

- `PRODUCTION_GUIDE.md` - Guía completa de producción
- `docker-compose.prod.yml` - Configuración Docker
- `deploy.sh` - Script de deployment
- `backup.sh` - Script de backup automático
- `health_check.sh` - Monitoreo de salud

## 🔒 Configuración de Seguridad

### Variables Críticas a Cambiar
```bash
# En backend/.env.production
MONGO_URL=mongodb://admin:TU_PASSWORD_SEGURO@mongodb:27017/...
JWT_SECRET_KEY=tu-clave-secreta-super-segura

# En frontend/.env.production  
REACT_APP_BACKEND_URL=https://tudominio.com
```

### Credenciales Zaffex
- Obtener API keys reales en: https://zaffex.com
- Configurar en la aplicación: Configuración → Zaffex API

## 🎮 Modos de Uso

### 🟢 Modo Demo (Sin dinero real)
```
API Key: demo_api_key_12345678901234567890
API Secret: demo_api_secret_12345678901234567890
✅ Modo de prueba: ACTIVADO
```

### 🔴 Modo Real (Dinero real)
```
API Key: [Tu clave real de Zaffex]  
API Secret: [Tu secreto real de Zaffex]
❌ Modo de prueba: DESACTIVADO
```

## ⚡ Funcionalidades Completas

- ✅ 6 estrategias de trading automatizado
- ✅ Integración real con broker Zaffex
- ✅ Dashboard en tiempo real
- ✅ Gestión completa de portfolio
- ✅ Sistema de backup automático
- ✅ Monitoreo y health checks
- ✅ SSL/HTTPS configurado
- ✅ Escalable y listo para producción

## 🚨 Advertencias Importantes

**⚠️ RIESGO FINANCIERO REAL**
- En modo real, los bots usan dinero verdadero
- Comienza con cantidades pequeñas ($10-50)
- Configura stop-loss en todos los bots
- Monitorea constantemente las operaciones

## 📞 Soporte

Para problemas técnicos:
1. Revisar logs: `docker-compose logs -f`
2. Health check: `./health_check.sh`  
3. Consultar: `PRODUCTION_GUIDE.md`

---

**¡Tu plataforma de trading automatizado está lista para generar ganancias reales!** 🚀

*Desarrollado con ❤️ para trading automatizado profesional*
"""

def create_quick_setup_script():
    """Crear script de setup ultra rápido"""
    return """#!/bin/bash

# GPTading Pro - Quick Production Setup

echo "🚀 GPTading Pro - Quick Setup"
echo "=============================="

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
else
    echo "✅ Docker found"
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose found"
fi

# Hacer scripts ejecutables
chmod +x deploy.sh backup.sh health_check.sh

# Crear directorios necesarios
mkdir -p logs backups frontend/ssl

echo ""
echo "✅ Setup completed!"
echo ""
echo "🔧 NEXT STEPS:"
echo "1. Edit backend/.env.production (change passwords)"
echo "2. Edit frontend/.env.production (set your domain)"
echo "3. Configure SSL: frontend/ssl/ (cert.pem, key.pem)"
echo "4. Deploy: ./deploy.sh"
echo ""
echo "📚 READ: PRODUCTION_GUIDE.md for complete instructions"
echo ""
echo "🎉 Ready to deploy!"
"""

def add_production_configs(zipf):
    """Agregar configuraciones adicionales de producción"""
    
    # Configuración de Nginx optimizada
    nginx_optimized = """events {
    worker_connections 2048;
    use epoll;
    multi_accept on;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    upstream backend {
        server backend:8001;
        keepalive 32;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    
    server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;
        
        # Security headers
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        
        # Frontend static files
        location / {
            try_files $uri $uri/ /index.html;
            expires 1h;
            add_header Cache-Control "public, immutable";
        }
        
        # API routes with rate limiting
        location /api {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";
            proxy_http_version 1.1;
            
            # Timeouts
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }
        
        # Health check
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
    }
}
"""
    
    zipf.writestr("frontend/nginx.optimized.conf", nginx_optimized)
    
    # Docker Compose optimizado para producción
    docker_compose_optimized = """version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: gptading_mongodb
    restart: unless-stopped
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD:-secure_password_change_me}
      MONGO_INITDB_DATABASE: gptading_pro_prod
    networks:
      - gptading_network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: gptading_backend
    restart: unless-stopped
    environment:
      - MONGO_URL=mongodb://admin:${MONGO_ROOT_PASSWORD:-secure_password_change_me}@mongodb:27017/gptading_pro_prod?authSource=admin
      - DB_NAME=gptading_pro_prod
      - JWT_SECRET_KEY=${JWT_SECRET_KEY:-change-this-in-production}
      - LOG_LEVEL=INFO
    depends_on:
      - mongodb
    networks:
      - gptading_network
    volumes:
      - ./logs:/var/log/gptading
    logging:
      driver: "json-file"  
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: gptading_frontend
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    networks:
      - gptading_network
    volumes:
      - ./frontend/ssl:/etc/nginx/ssl:ro
    logging:
      driver: "json-file"
      options:
        max-size: "10m" 
        max-file: "3"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mongodb_data:

networks:
  gptading_network:
    driver: bridge
"""
    
    zipf.writestr("docker-compose.optimized.yml", docker_compose_optimized)
    
    print("✅ Configuraciones de producción optimizadas agregadas")

if __name__ == "__main__":
    package_file = create_production_package()
    print(f"\n🎯 PAQUETE CREADO: {package_file}")
    print("📤 ¡Listo para subir a tu servidor de producción!")