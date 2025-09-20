#!/bin/bash

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
