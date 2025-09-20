# 🚀 GPTading Pro - Guía de Producción

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
