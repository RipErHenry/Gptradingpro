#!/usr/bin/env python3
"""
GPTading Pro - Production Deployment Script
Prepara la aplicación para hosting real
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

def create_production_env():
    """Crear configuraciones de producción"""
    print("🔧 Creando configuraciones de producción...")
    
    # Backend production .env
    backend_prod_env = """# GPTading Pro - Production Environment
# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=gptading_pro_prod

# Security
JWT_SECRET_KEY=change-this-to-a-secure-random-string-in-production
CORS_ORIGINS=["https://yourdomain.com"]

# Zaffex API (Real)
ZAFFEX_BASE_URL=https://api.zaffex.com
ZAFFEX_WS_URL=wss://stream.zaffex.com

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/gptading/backend.log

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=100
"""
    
    with open("backend/.env.production", "w") as f:
        f.write(backend_prod_env)
    
    # Frontend production .env
    frontend_prod_env = """# GPTading Pro Frontend - Production
REACT_APP_BACKEND_URL=https://yourdomain.com
REACT_APP_VERSION=1.0.0
REACT_APP_ENVIRONMENT=production
GENERATE_SOURCEMAP=false
"""
    
    with open("frontend/.env.production", "w") as f:
        f.write(frontend_prod_env)
    
    print("✅ Configuraciones de producción creadas")

def create_docker_config():
    """Crear configuración Docker para producción"""
    print("🐳 Creando configuración Docker...")
    
    # Dockerfile para backend
    backend_dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8001

# Comando para ejecutar
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
"""
    
    with open("backend/Dockerfile", "w") as f:
        f.write(backend_dockerfile)
    
    # Dockerfile para frontend
    frontend_dockerfile = """FROM node:18-alpine as build

WORKDIR /app

# Copiar package.json y yarn.lock
COPY package*.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copiar código y construir
COPY . .
RUN yarn build

# Imagen de producción con Nginx
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
    
    with open("frontend/Dockerfile", "w") as f:
        f.write(frontend_dockerfile)
    
    # Configuración Nginx
    nginx_config = """events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    upstream backend {
        server backend:8001;
    }
    
    server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;
        
        # Frontend routes
        location / {
            try_files $uri $uri/ /index.html;
        }
        
        # API routes
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # WebSocket support
        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
"""
    
    with open("frontend/nginx.conf", "w") as f:
        f.write(nginx_config)
    
    # Docker Compose para orquestación completa
    docker_compose = """version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: gptading_mongodb
    restart: unless-stopped
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secure_password_change_me
    networks:
      - gptading_network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: gptading_backend
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://admin:secure_password_change_me@mongodb:27017/gptading_pro_prod?authSource=admin
      - DB_NAME=gptading_pro_prod
    depends_on:
      - mongodb
    networks:
      - gptading_network
    volumes:
      - ./logs:/var/log/gptading

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
  mongodb_data:

networks:
  gptading_network:
    driver: bridge
"""
    
    with open("docker-compose.prod.yml", "w") as f:
        f.write(docker_compose)
    
    print("✅ Configuración Docker creada")

def create_deployment_scripts():
    """Crear scripts de deployment"""
    print("🚀 Creando scripts de deployment...")
    
    # Script de deploy simple
    deploy_script = """#!/bin/bash

# GPTading Pro - Production Deployment Script

echo "🚀 Deploying GPTading Pro to Production..."

# Parar servicios existentes
echo "📛 Stopping existing services..."
docker-compose -f docker-compose.prod.yml down

# Construir imágenes
echo "🏗️ Building Docker images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Iniciar servicios
echo "▶️ Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Verificar estado
echo "🔍 Checking service status..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ Deployment completed!"
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"

# Mostrar logs en tiempo real
echo "📋 Showing logs (Ctrl+C to exit)..."
docker-compose -f docker-compose.prod.yml logs -f
"""
    
    with open("deploy.sh", "w") as f:
        f.write(deploy_script)
    os.chmod("deploy.sh", 0o755)
    
    # Script de backup
    backup_script = """#!/bin/bash

# GPTading Pro - Database Backup Script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
BACKUP_FILE="gptading_backup_$DATE.gz"

echo "💾 Creating backup: $BACKUP_FILE"

# Crear directorio de backups
mkdir -p $BACKUP_DIR

# Hacer backup de MongoDB
docker exec gptading_mongodb mongodump --authenticationDatabase admin -u admin -p secure_password_change_me --db gptading_pro_prod --archive --gzip > $BACKUP_DIR/$BACKUP_FILE

echo "✅ Backup completed: $BACKUP_DIR/$BACKUP_FILE"

# Limpiar backups antiguos (mantener solo los últimos 7 días)
find $BACKUP_DIR -name "gptading_backup_*.gz" -mtime +7 -delete

echo "🧹 Old backups cleaned up"
"""
    
    with open("backup.sh", "w") as f:
        f.write(backup_script)
    os.chmod("backup.sh", 0o755)
    
    print("✅ Scripts de deployment creados")

def update_backend_for_production():
    """Actualizar backend para producción"""
    print("🔧 Actualizando backend para producción...")
    
    # Actualizar server.py para usar el nuevo servicio
    server_update = """# Importar el servicio de producción en lugar del de demo
from services.production_zaffex_service import production_zaffex_service

# En los routers, reemplazar:
# from ..services.zaffex_service import zaffex_service
# por:
# from services.production_zaffex_service import production_zaffex_service as zaffex_service
"""
    
    # Actualizar las rutas para usar el servicio de producción
    routes_files = [
        "backend/routes/bots.py",
        "backend/routes/zaffex.py", 
        "backend/routes/portfolio.py"
    ]
    
    for route_file in routes_files:
        if os.path.exists(route_file):
            with open(route_file, 'r') as f:
                content = f.read()
            
            # Reemplazar import del servicio
            content = content.replace(
                "from services.zaffex_service import zaffex_service",
                "from services.production_zaffex_service import production_zaffex_service as zaffex_service"
            )
            
            with open(route_file, 'w') as f:
                f.write(content)
    
    print("✅ Backend actualizado para producción")

def create_ssl_config():
    """Crear configuración SSL/HTTPS"""
    print("🔒 Creando configuración SSL...")
    
    ssl_nginx_config = """events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    upstream backend {
        server backend:8001;
    }
    
    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }
    
    # HTTPS Configuration
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;
        
        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        # Security Headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-XSS-Protection "1; mode=block" always;
        
        root /usr/share/nginx/html;
        index index.html;
        
        # Frontend routes
        location / {
            try_files $uri $uri/ /index.html;
        }
        
        # API routes
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Security
            proxy_hide_header X-Powered-By;
        }
        
        # WebSocket support
        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
"""
    
    with open("frontend/nginx.ssl.conf", "w") as f:
        f.write(ssl_nginx_config)
    
    print("✅ Configuración SSL creada")

def create_monitoring_config():
    """Crear configuración de monitoreo"""
    print("📊 Creando configuración de monitoreo...")
    
    # Script de health check
    health_check = """#!/bin/bash

# GPTading Pro - Health Check Script

echo "🔍 GPTading Pro Health Check"
echo "=============================="

# Check Frontend
echo "📱 Checking Frontend..."
if curl -f -s http://localhost > /dev/null; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: FAILED"
fi

# Check Backend
echo "🔧 Checking Backend API..."
if curl -f -s http://localhost:8001/api/health > /dev/null; then
    echo "✅ Backend API: OK"
else
    echo "❌ Backend API: FAILED" 
fi

# Check Database
echo "🗄️ Checking Database..."
if docker exec gptading_mongodb mongosh --quiet --eval "db.runCommand('ping')" > /dev/null 2>&1; then
    echo "✅ Database: OK"
else
    echo "❌ Database: FAILED"
fi

# Check Docker Services
echo "🐳 Checking Docker Services..."
docker-compose -f docker-compose.prod.yml ps

echo "=============================="
echo "Health check completed!"
"""
    
    with open("health_check.sh", "w") as f:
        f.write(health_check)
    os.chmod("health_check.sh", 0o755)
    
    print("✅ Configuración de monitoreo creada")

def create_production_guide():
    """Crear guía de producción"""
    guide = """# 🚀 GPTading Pro - Guía de Producción

## 📋 Pre-requisitos del Servidor

### Sistema Operativo
- Ubuntu 20.04+ o CentOS 8+
- Mínimo 2 CPU cores, 4GB RAM, 20GB SSD

### Software Requerido
```bash
# Instalar Docker y Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 🎯 Deployment Paso a Paso

### 1. Preparar Servidor
```bash
# Crear directorio de la aplicación
sudo mkdir /opt/gptading-pro
sudo chown $USER:$USER /opt/gptading-pro
cd /opt/gptading-pro

# Clonar o subir archivos de la aplicación
# git clone [tu-repositorio] .
```

### 2. Configurar Variables de Entorno
```bash
# Editar configuraciones
nano backend/.env.production
nano frontend/.env.production

# IMPORTANTE: Cambiar:
# - MongoDB password 
# - JWT secret
# - Domain name
# - SSL certificates path
```

### 3. Configurar SSL/HTTPS (Recomendado)
```bash
# Opción A: Let's Encrypt (Gratuito)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Copiar certificados
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem frontend/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem frontend/ssl/key.pem

# Usar configuración SSL
cp frontend/nginx.ssl.conf frontend/nginx.conf
```

### 4. Desplegar la Aplicación
```bash
# Desplegar en producción
./deploy.sh

# O manualmente:
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Verificar Deployment
```bash
# Health check
./health_check.sh

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Configuraciones de Producción

### Dominios y DNS
```
# Configurar registros DNS:
A    yourdomain.com      -> [IP-del-servidor]  
A    www.yourdomain.com  -> [IP-del-servidor]
```

### Firewall
```bash
# Configurar UFW
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Backup Automático
```bash
# Configurar crontab para backup diario
crontab -e

# Agregar línea:
0 2 * * * /opt/gptading-pro/backup.sh
```

## 🔒 Seguridad

### 1. Configuración MongoDB
- Cambiar credenciales por defecto
- Habilitar autenticación
- Configurar red interna solamente

### 2. Configuración API Zaffex
- Restricción de IP en Zaffex
- Permisos mínimos necesarios
- Rotación periódica de keys

### 3. Configuración Nginx
- Rate limiting habilitado
- Security headers configurados
- SSL/TLS moderno

## 📊 Monitoreo

### Logs de la Aplicación
```bash
# Ver logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker logs gptading_frontend
docker logs gptading_backend
docker logs gptading_mongodb
```

### Health Checks
```bash
# Ejecutar health check
./health_check.sh

# Configurar monitoreo automático (opcional)
# - Uptime Robot
# - New Relic
# - DataDog
```

## 🚨 Solución de Problemas

### Frontend no carga
```bash
# Verificar contenedor
docker ps | grep frontend
docker logs gptading_frontend

# Verificar configuración Nginx
docker exec gptading_frontend nginx -t
```

### Backend API no responde
```bash
# Verificar contenedor
docker ps | grep backend
docker logs gptading_backend

# Verificar conectividad MongoDB
docker exec gptading_backend ping mongodb
```

### Base de datos no conecta
```bash
# Verificar MongoDB
docker exec gptading_mongodb mongosh

# Verificar credenciales
docker logs gptading_mongodb
```

## 🔄 Actualizaciones

### Actualizar la Aplicación
```bash
# Parar servicios
docker-compose -f docker-compose.prod.yml down

# Actualizar código
git pull origin main

# Reconstruir y desplegar
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Backup antes de Actualizar
```bash
# Siempre hacer backup
./backup.sh

# Verificar backup
ls -la backups/
```

## 📞 URLs de Producción

- 🌐 **Frontend**: https://yourdomain.com
- 🔧 **API Backend**: https://yourdomain.com/api
- 📚 **Documentación**: https://yourdomain.com/api/docs
- 💾 **Health Check**: https://yourdomain.com/api/health

## ⚡ Rendimiento

### Optimizaciones Recomendadas
- CDN para assets estáticos
- Redis para caché (opcional)
- Load balancer para múltiples instancias
- Database indexing optimizado

### Escalabilidad
- Usar múltiples workers de backend
- Réplicas de base de datos
- Separación de microservicios

---

**¡Tu GPTading Pro está listo para producción!** 🚀

Para soporte técnico, revisar logs y documentación de troubleshooting.
"""
    
    with open("PRODUCTION_GUIDE.md", "w") as f:
        f.write(guide)
    
    print("✅ Guía de producción creada")

def main():
    """Función principal"""
    print("🎯 GPTading Pro - Production Deployment Setup")
    print("=" * 60)
    
    # Ejecutar todas las configuraciones
    create_production_env()
    create_docker_config()
    create_deployment_scripts()
    update_backend_for_production()
    create_ssl_config()
    create_monitoring_config()
    create_production_guide()
    
    print("\n🎉" + "=" * 50 + "🎉")
    print("   ¡GPTading Pro LISTO para PRODUCCIÓN!")
    print("🎉" + "=" * 50 + "🎉")
    
    print("\n📋 ARCHIVOS CREADOS:")
    files = [
        "✅ docker-compose.prod.yml",
        "✅ deploy.sh", 
        "✅ backup.sh",
        "✅ health_check.sh",
        "✅ backend/Dockerfile",
        "✅ frontend/Dockerfile", 
        "✅ frontend/nginx.conf",
        "✅ PRODUCTION_GUIDE.md"
    ]
    for file in files:
        print(f"   {file}")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("   1. Configurar dominio y SSL")
    print("   2. Editar variables de entorno")
    print("   3. Ejecutar: ./deploy.sh")
    print("   4. Verificar: ./health_check.sh")
    
    print("\n📚 DOCUMENTACIÓN:")
    print("   Leer: PRODUCTION_GUIDE.md")
    
    print("\n✨ ¡Listo para hosting real! ✨")

if __name__ == "__main__":
    main()