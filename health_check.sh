#!/bin/bash

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
