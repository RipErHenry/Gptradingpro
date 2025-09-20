"""
Integración Real con Zaffex - Para Trading en Vivo
⚠️ ADVERTENCIA: Este código maneja dinero real
"""

import aiohttp
import asyncio
import hmac
import hashlib
import time
import json
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RealZaffexIntegration:
    """
    Integración real con Zaffex Broker
    ⚠️ USO BAJO TU PROPIO RIESGO
    """
    
    def __init__(self):
        # URLs oficiales de Zaffex (verificar en su documentación)
        self.base_url = "https://api.zaffex.com"  # URL base real
        self.ws_url = "wss://stream.zaffex.com"   # WebSocket real
        self.connected_users = {}
        
    async def validate_real_credentials(self, api_key: str, api_secret: str) -> dict:
        """
        Validar credenciales reales con Zaffex
        """
        try:
            # Preparar request de validación
            timestamp = str(int(time.time() * 1000))
            
            # Crear signature según documentación de Zaffex
            query_string = f"timestamp={timestamp}"
            signature = hmac.new(
                api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'X-ZAFFEX-APIKEY': api_key,
                'X-ZAFFEX-SIGNATURE': signature,
                'Content-Type': 'application/json'
            }
            
            async with aiohttp.ClientSession() as session:
                # Test endpoint de account info
                async with session.get(
                    f"{self.base_url}/api/v3/account",
                    headers=headers,
                    params={'timestamp': timestamp}
                ) as response:
                    
                    if response.status == 200:
                        account_data = await response.json()
                        return {
                            'valid': True,
                            'account_type': account_data.get('accountType', 'SPOT'),
                            'permissions': account_data.get('permissions', []),
                            'balance_count': len(account_data.get('balances', [])),
                            'can_trade': 'SPOT' in account_data.get('permissions', []),
                            'message': 'Credenciales válidas'
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'valid': False,
                            'error_code': error_data.get('code', 'UNKNOWN'),
                            'message': error_data.get('msg', 'Error de validación')
                        }
                        
        except Exception as e:
            logger.error(f"Error validating Zaffex credentials: {e}")
            return {
                'valid': False,
                'message': f'Error de conexión: {str(e)}'
            }
    
    async def get_real_account_info(self, api_key: str, api_secret: str) -> dict:
        """
        Obtener información real de la cuenta
        """
        try:
            timestamp = str(int(time.time() * 1000))
            query_string = f"timestamp={timestamp}"
            signature = hmac.new(
                api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'X-ZAFFEX-APIKEY': api_key,
                'X-ZAFFEX-SIGNATURE': signature
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v3/account",
                    headers=headers,
                    params={'timestamp': timestamp}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Procesar balances
                        total_balance = 0
                        available_balance = 0
                        
                        for balance in data.get('balances', []):
                            if balance['asset'] == 'USDT':
                                total_balance = float(balance['free']) + float(balance['locked'])
                                available_balance = float(balance['free'])
                        
                        return {
                            'success': True,
                            'account_type': data.get('accountType'),
                            'total_balance': total_balance,
                            'available_balance': available_balance,
                            'in_orders': total_balance - available_balance,
                            'permissions': data.get('permissions', []),
                            'can_trade': 'SPOT' in data.get('permissions', [])
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('msg', 'Error desconocido')
                        }
                        
        except Exception as e:
            return {
                'success': False, 
                'error': f'Error de conexión: {str(e)}'
            }
    
    async def get_real_market_prices(self, symbols: List[str]) -> List[dict]:
        """
        Obtener precios reales del mercado
        """
        try:
            market_data = []
            
            async with aiohttp.ClientSession() as session:
                # Obtener todos los tickers
                async with session.get(f"{self.base_url}/api/v3/ticker/24hr") as response:
                    if response.status == 200:
                        tickers = await response.json()
                        
                        # Filtrar por símbolos solicitados
                        for symbol in symbols:
                            zaffex_symbol = symbol.replace('/', '')  # BTC/USDT -> BTCUSDT
                            
                            for ticker in tickers:
                                if ticker['symbol'] == zaffex_symbol:
                                    market_data.append({
                                        'symbol': symbol,
                                        'price': float(ticker['lastPrice']),
                                        'change_24h': float(ticker['priceChangePercent']),
                                        'volume_24h': float(ticker['volume']),
                                        'high_24h': float(ticker['highPrice']),
                                        'low_24h': float(ticker['lowPrice']),
                                        'timestamp': datetime.utcnow()
                                    })
                                    break
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error getting real market data: {e}")
            return []
    
    async def place_real_order(self, api_key: str, api_secret: str, order_data: dict) -> dict:
        """
        ⚠️ COLOCAR ORDEN REAL - USA DINERO REAL
        """
        try:
            timestamp = str(int(time.time() * 1000))
            
            # Preparar parámetros de la orden
            params = {
                'symbol': order_data['symbol'].replace('/', ''),  # BTC/USDT -> BTCUSDT
                'side': order_data['side'].upper(),  # BUY or SELL
                'type': 'MARKET',  # Orden de mercado
                'quantity': f"{order_data['quantity']:.8f}",
                'timestamp': timestamp
            }
            
            # Crear query string para signature
            query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
            signature = hmac.new(
                api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'X-ZAFFEX-APIKEY': api_key,
                'X-ZAFFEX-SIGNATURE': signature,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            logger.warning(f"⚠️ COLOCANDO ORDEN REAL: {params}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v3/order",
                    headers=headers,
                    data=params
                ) as response:
                    
                    result = await response.json()
                    
                    if response.status == 200:
                        return {
                            'success': True,
                            'order_id': result.get('orderId'),
                            'symbol': order_data['symbol'],
                            'side': result.get('side'),
                            'quantity': float(result.get('executedQty', 0)),
                            'price': float(result.get('price', 0)),
                            'status': result.get('status'),
                            'fees': float(result.get('fills', [{}])[0].get('commission', 0)) if result.get('fills') else 0,
                            'timestamp': timestamp
                        }
                    else:
                        return {
                            'success': False,
                            'error': result.get('msg', 'Error en orden'),
                            'code': result.get('code')
                        }
                        
        except Exception as e:
            logger.error(f"Error placing real order: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_order_history(self, api_key: str, api_secret: str, symbol: str = None, limit: int = 100) -> dict:
        """
        Obtener historial real de órdenes
        """
        try:
            timestamp = str(int(time.time() * 1000))
            
            params = {
                'timestamp': timestamp,
                'limit': str(limit)
            }
            
            if symbol:
                params['symbol'] = symbol.replace('/', '')
            
            query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
            signature = hmac.new(
                api_secret.encode('utf-8'),
                query_string.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'X-ZAFFEX-APIKEY': api_key,
                'X-ZAFFEX-SIGNATURE': signature
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v3/allOrders",
                    headers=headers,
                    params=params
                ) as response:
                    
                    if response.status == 200:
                        orders = await response.json()
                        return {
                            'success': True,
                            'orders': orders,
                            'count': len(orders)
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('msg', 'Error obteniendo historial')
                        }
                        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Instancia para usar en producción
real_zaffex = RealZaffexIntegration()


# INSTRUCCIONES DE USO:
"""
⚠️ ADVERTENCIAS IMPORTANTES:

1. TESTING PRIMERO:
   - Usa siempre el modo testnet de Zaffex primero
   - Verifica que todo funcione con cantidades mínimas
   
2. CONFIGURACIÓN SEGURA:
   - Restringe las IPs en tu API key de Zaffex
   - Usa permisos mínimos necesarios (solo SPOT trading)
   - NO compartas tus credenciales API
   
3. GESTIÓN DE RIESGO:
   - Comienza con cantidades muy pequeñas
   - Configura stop-loss en todos los bots
   - Monitorea constantemente las operaciones
   
4. IMPLEMENTACIÓN:
   - Reemplaza zaffex_service con real_zaffex en routes/
   - Configura logging detallado
   - Implementa alertas de emergencia

EJEMPLO DE USO:
```python
# Validar credenciales
result = await real_zaffex.validate_real_credentials(api_key, api_secret)

# Obtener balance real  
balance = await real_zaffex.get_real_account_info(api_key, api_secret)

# ⚠️ Colocar orden real
order = await real_zaffex.place_real_order(api_key, api_secret, {
    'symbol': 'BTC/USDT',
    'side': 'BUY', 
    'quantity': 0.001  # Cantidad muy pequeña para pruebas
})
```

⚠️ USA BAJO TU PROPIO RIESGO ⚠️
"""