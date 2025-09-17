#!/usr/bin/env python3
"""
GPTading Pro - Script de Empaquetado
Comprime toda la aplicación en un archivo ZIP para distribución
"""

import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

def create_gptading_package():
    """Crear paquete completo de GPTading Pro"""
    
    # Directorio base de la aplicación
    base_dir = Path(__file__).parent
    
    # Nombre del archivo de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"gptading_pro_{timestamp}.zip"
    
    # Archivos y carpetas a incluir
    includes = [
        "frontend/",
        "backend/", 
        "README.md",
        "contracts.md",
        "package_app.py",
        "run_app.py"
    ]
    
    # Archivos y carpetas a excluir
    excludes = [
        "__pycache__",
        "node_modules", 
        ".git",
        ".env",
        "*.log",
        ".DS_Store",
        "build/",
        "dist/",
        "*.pyc"
    ]
    
    print(f"🚀 Empaquetando GPTading Pro...")
    print(f"📦 Archivo de salida: {output_filename}")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Agregar archivos del proyecto
        for include_pattern in includes:
            include_path = base_dir / include_pattern
            
            if include_path.is_file():
                # Archivo individual
                zipf.write(include_path, include_pattern)
                print(f"✅ Agregado: {include_pattern}")
                
            elif include_path.is_dir():
                # Directorio completo
                for root, dirs, files in os.walk(include_path):
                    # Filtrar directorios excluidos
                    dirs[:] = [d for d in dirs if not any(ex in d for ex in excludes)]
                    
                    for file in files:
                        # Filtrar archivos excluidos
                        if any(ex in file for ex in excludes):
                            continue
                            
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(base_dir)
                        zipf.write(file_path, arc_name)
                        
                print(f"✅ Agregado directorio: {include_pattern}")
        
        # Agregar archivo de instrucciones
        instructions = """
# GPTading Pro - Instrucciones de Instalación

## 🚀 Instalación Rápida

### 1. Instalar Dependencias Backend (Python)
```bash
cd backend
pip install -r requirements.txt
```

### 2. Instalar Dependencias Frontend (React)  
```bash
cd frontend
npm install
# o
yarn install
```

### 3. Configurar Variables de Entorno
Crear archivo `.env` en `/backend/` con:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=gptading_pro
```

Crear archivo `.env` en `/frontend/` con:
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

### 4. Ejecutar Aplicación
```bash
# Terminal 1 - Backend
cd backend  
uvicorn server:app --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
npm start
# o 
yarn start
```

### 5. Acceder a la Aplicación
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/docs

## 📋 Funcionalidades
- ✅ Trading automatizado con 6 estrategias
- ✅ Integración simulada con Zaffex broker
- ✅ Dashboard de métricas en tiempo real
- ✅ Gestión completa de bots de trading
- ✅ Portfolio tracking y análisis
- ✅ API REST completa

## 🔧 Para Producción
1. Configurar MongoDB real
2. Obtener credenciales API de Zaffex
3. Configurar SSL/HTTPS
4. Implementar autenticación JWT

¡Listo para usar! 🎉
"""
        
        zipf.writestr("INSTRUCCIONES.md", instructions)
        
    print(f"🎉 ¡Empaquetado completado!")
    print(f"📁 Archivo generado: {output_filename}")
    print(f"📏 Tamaño: {os.path.getsize(output_filename) / (1024*1024):.1f} MB")
    
    return output_filename

if __name__ == "__main__":
    package_file = create_gptading_package()
    print(f"\n🚀 Para usar tu aplicación:")
    print(f"1. Descomprime: {package_file}")  
    print(f"2. Sigue las instrucciones en INSTRUCCIONES.md")
    print(f"3. Ejecuta: python run_app.py")