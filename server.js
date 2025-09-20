#!/usr/bin/env node
/**
 * GPTading Pro - Servidor Express
 * Ejecuta la aplicación como una web app profesional
 */

const express = require('express');
const path = require('path');
const open = require('open');

const app = express();
const PORT = process.env.PORT || 3333;

// Configurar Express para servir archivos estáticos
app.use(express.static(__dirname));

// Ruta principal - servir index.html sin mostrarlo en URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API endpoints para futuras expansiones
app.get('/api/status', (req, res) => {
    res.json({
        status: 'online',
        app: 'GPTading Pro',
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

// Middleware para manejar errores 404
app.use((req, res) => {
    res.status(404).sendFile(path.join(__dirname, 'index.html'));
});

// Iniciar servidor
app.listen(PORT, () => {
    const serverUrl = `http://localhost:${PORT}`;
    
    console.log('🚀 GPTading Pro - Express Server');
    console.log('=' + '='.repeat(48) + '=');
    console.log(`✅ Servidor iniciado: ${serverUrl}`);
    console.log(`📱 GPTading Pro: ${serverUrl}`);
    console.log(`🔧 API Status: ${serverUrl}/api/status`);
    console.log('🛑 Para detener: Ctrl+C');
    console.log('=' + '='.repeat(48) + '=');
    
    // Abrir navegador automáticamente
    setTimeout(() => {
        open(serverUrl).catch(err => {
            console.log('❌ No se pudo abrir el navegador automáticamente');
            console.log(`📌 Abre manualmente: ${serverUrl}`);
        });
    }, 1500);
});

// Manejo de cierre graceful
process.on('SIGINT', () => {
    console.log('\n🛑 Cerrando GPTading Pro Server...');
    console.log('👋 ¡Hasta luego!');
    process.exit(0);
});