#!/bin/bash

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
