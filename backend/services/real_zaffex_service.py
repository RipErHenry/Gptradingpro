"""
Servicio Real de Zaffex - Para uso en producción
Reemplaza la simulación con conexión real al broker
"""
import aiohttp
import asyncio
import hmac
import hashlib
import time
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class RealZaffexService:
    """
    Servicio real para integración con Zaffex Broker
    IMPORTANTE: Requiere credenciales API reales de Zaffex
    """
    
    def __init__(self):
        self.base_url = "https://api.zaffex.com"  # URL real de Zaffex API
        self.connected_users = {}
        
    def _generate_signature(self, api_secret: str, params: str) -> str:
        """Generar firma HMAC para autenticación"""
        return hmac.new(
            api_secret.encode('utf-8'), 
            params.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
    
    async def validate_credentials(self, api_key: str, api_secret: str) -> bool:
        """Validar credenciales reales con Zaffex"""
        try:
            # Hacer llamada real a Zaffex API para validar
            timestamp = str(int(time.time() * 1000))
            params = f"timestamp={timestamp}"
            signature = self._generate_signature(api_secret, params)
            
            headers = {
                'X-ZAFFEX-APIKEY': api_key,
                'X-ZAFFEX-SIGNATURE': signature
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/account", 
                    headers=headers,
                    params={'timestamp': timestamp}
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error validating Zaffex credentials: {e}")
            return False
    
    async def get_account_balance(self, user_id: str) -> Dict:
        """Obtener balance real de Zaffex"""
        if user_id not in self.connected_users:
            raise Exception("Usuario no conectado a Zaffex")
            
        credentials = self.connected_users[user_id]
        
        try:
            timestamp = str(int(time.time() * 1000))
            params = f"timestamp={timestamp}"
            signature = self._generate_signature(credentials['api_secret'], params)
            
            headers = {
                'X-ZAFFEX-APIKEY': credentials['api_key'],
                'X-ZAFFEX-SIGNATURE': signature
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/v1/account/balance",
                    headers=headers,
                    params={'timestamp': timestamp}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "total_balance": float(data.get('totalWalletBalance', 0)),
                            "available_balance": float(data.get('availableBalance', 0)),
                            "in_orders": float(data.get('totalPositionInitialMargin', 0)),
                            "currency": "USDT"
                        }
                    else:
                        raise Exception(f"Error obteniendo balance: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error getting Zaffex balance: {e}")
            raise e
    
    async def get_market_data(self, symbols: List[str]) -> List[Dict]:
        """Obtener datos reales de mercado de Zaffex"""
        try:
            market_data = []
            
            async with aiohttp.ClientSession() as session:
                for symbol in symbols:
                    # Convertir formato (BTC/USDT -> BTCUSDT)
                    zaffex_symbol = symbol.replace('/', '')
                    
                    async with session.get(
                        f"{self.base_url}/api/v1/ticker/24hr",
                        params={'symbol': zaffex_symbol}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            market_data.append({
                                "symbol": symbol,
                                "price": float(data.get('lastPrice', 0)),
                                "change_24h": float(data.get('priceChangePercent', 0)),
                                "volume_24h": f"{float(data.get('volume', 0)):.0f}",
                                "last_updated": time.time()
                            })
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return []
    
    async def place_order(self, user_id: str, order_data: Dict) -> Dict:
        """Colocar orden real en Zaffex"""
        if user_id not in self.connected_users:
            raise Exception("Usuario no conectado a Zaffex")
            
        credentials = self.connected_users[user_id]
        
        try:
            timestamp = str(int(time.time() * 1000))
            
            # Preparar parámetros de la orden
            order_params = {
                'symbol': order_data['symbol'].replace('/', ''),
                'side': order_data['type'],  # BUY or SELL
                'type': 'MARKET',  # Orden de mercado
                'quantity': str(order_data['amount']),
                'timestamp': timestamp
            }
            
            # Generar firma
            params_string = '&'.join([f"{k}={v}" for k, v in sorted(order_params.items())])
            signature = self._generate_signature(credentials['api_secret'], params_string)
            
            headers = {
                'X-ZAFFEX-APIKEY': credentials['api_key'],
                'X-ZAFFEX-SIGNATURE': signature,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/v1/order",
                    headers=headers,
                    data=order_params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "order_id": data.get('orderId'),
                            "status": data.get('status', 'FILLED'),
                            "symbol": order_data['symbol'],
                            "type": order_data['type'],
                            "amount": float(data.get('executedQty', order_data['amount'])),
                            "price": float(data.get('price', order_data['price'])),
                            "total": float(data.get('cummulativeQuoteQty', 0)),
                            "executed_at": timestamp,
                            "fees": float(data.get('fees', 0))
                        }
                    else:
                        error_data = await response.json()
                        raise Exception(f"Error en orden: {error_data}")
                        
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            raise e
    
    def connect_user(self, user_id: str, api_key: str, api_secret: str):
        """Conectar usuario con credenciales reales"""
        self.connected_users[user_id] = {
            "api_key": api_key,
            "api_secret": api_secret,
            "connected_at": time.time()
        }
        logger.info(f"Usuario {user_id} conectado a Zaffex REAL")
    
    def disconnect_user(self, user_id: str):
        """Desconectar usuario"""
        if user_id in self.connected_users:
            del self.connected_users[user_id]
            logger.info(f"Usuario {user_id} desconectado de Zaffex REAL")

# Para usar en producción, importar esta clase en lugar de ZaffexService
real_zaffex_service = RealZaffexService()