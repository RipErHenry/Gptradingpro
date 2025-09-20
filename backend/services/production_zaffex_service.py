"""
Production Zaffex Service - Integración Real y Simulada
Maneja tanto el modo demo como el modo real automáticamente
"""

import aiohttp
import asyncio
import hmac
import hashlib
import time
import json
import random
from typing import Dict, List, Optional
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

class ProductionZaffexService:
    """
    Servicio de producción que maneja automáticamente modo demo y real
    """
    
    def __init__(self):
        self.base_url = "https://api.zaffex.com"
        self.testnet_url = "https://testnet.zaffex.com"  
        self.connected_users = {}
        
    def _is_demo_credentials(self, api_key: str, api_secret: str) -> bool:
        """Detectar si son credenciales demo"""
        return (api_key.startswith('demo_') or 
                api_secret.startswith('demo_') or
                'demo' in api_key.lower() or 
                'test' in api_key.lower())
    
    def _generate_signature(self, secret: str, params: str) -> str:
        """Generar signature HMAC SHA256"""
        return hmac.new(
            secret.encode('utf-8'),
            params.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
    
    async def validate_credentials(self, api_key: str, api_secret: str) -> bool:
        """Validar credenciales (demo o real automáticamente)"""
        
        # Modo Demo
        if self._is_demo_credentials(api_key, api_secret):
            await asyncio.sleep(1)  # Simular latencia
            return len(api_key) >= 20 and len(api_secret) >= 20
        
        # Modo Real - Validar con Zaffex
        try:
            timestamp = str(int(time.time() * 1000))
            query_string = f"timestamp={timestamp}"
            signature = self._generate_signature(api_secret, query_string)
            
            headers = {
                'X-ZAFFEX-APIKEY': api_key,
                'X-ZAFFEX-SIGNATURE': signature,
                'Content-Type': 'application/json'
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    f"{self.base_url}/api/v3/account",
                    headers=headers,
                    params={'timestamp': timestamp}
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"Error validating real credentials: {e}")
            return False
    
    async def get_account_balance(self, user_id: str) -> Dict:
        """Obtener balance (demo o real)"""
        if user_id not in self.connected_users:
            raise Exception("Usuario no conectado a Zaffex")
        
        credentials = self.connected_users[user_id]
        
        # Modo Demo
        if self._is_demo_credentials(credentials['api_key'], credentials['api_secret']):
            return {
                "total_balance": round(random.uniform(5000, 50000), 2),
                "available_balance": round(random.uniform(3000, 30000), 2), 
                "in_orders": round(random.uniform(1000, 10000), 2),
                "currency": "USDT",
                "mode": "demo"
            }
        
        # Modo Real
        try:
            timestamp = str(int(time.time() * 1000))
            query_string = f"timestamp={timestamp}"
            signature = self._generate_signature(credentials['api_secret'], query_string)
            
            headers = {
                'X-ZAFFEX-APIKEY': credentials['api_key'],
                'X-ZAFFEX-SIGNATURE': signature
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    f"{self.base_url}/api/v3/account",
                    headers=headers,
                    params={'timestamp': timestamp}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        total_balance = 0
                        available_balance = 0
                        
                        for balance in data.get('balances', []):
                            if balance['asset'] == 'USDT':
                                available_balance = float(balance['free'])
                                total_balance = available_balance + float(balance['locked'])
                                break
                        
                        return {
                            "total_balance": total_balance,
                            "available_balance": available_balance,
                            "in_orders": total_balance - available_balance,
                            "currency": "USDT", 
                            "mode": "real"
                        }
                    else:
                        raise Exception(f"Error de API: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error getting real balance: {e}")
            raise e
    
    async def get_market_data(self, symbols: List[str]) -> List[Dict]:
        """Obtener datos de mercado (demo o real)"""
        
        # Para demo siempre usar datos simulados
        if not symbols:
            symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT", "DOT/USDT"]
        
        try:
            # Intentar obtener datos reales primero
            market_data = []
            
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{self.base_url}/api/v3/ticker/24hr") as response:
                    if response.status == 200:
                        tickers = await response.json()
                        
                        for symbol in symbols:
                            zaffex_symbol = symbol.replace('/', '')
                            
                            for ticker in tickers:
                                if ticker['symbol'] == zaffex_symbol:
                                    market_data.append({
                                        "symbol": symbol,
                                        "price": float(ticker['lastPrice']),
                                        "change_24h": float(ticker['priceChangePercent']),
                                        "volume_24h": f"{float(ticker['volume']):.0f}",
                                        "last_updated": datetime.utcnow(),
                                        "mode": "real"
                                    })
                                    break
                        
                        if market_data:
                            return market_data
            
        except Exception as e:
            logger.warning(f"Could not get real market data, using demo: {e}")
        
        # Fallback a datos demo
        base_prices = {
            "BTC/USDT": 43250,
            "ETH/USDT": 2580, 
            "ADA/USDT": 0.485,
            "DOT/USDT": 7.85,
            "MATIC/USDT": 0.92,
            "AVAX/USDT": 39.67
        }
        
        market_data = []
        for symbol in symbols:
            if symbol in base_prices:
                base_price = base_prices[symbol]
                change = random.uniform(-5, 5)
                current_price = base_price * (1 + change / 100)
                
                market_data.append({
                    "symbol": symbol,
                    "price": round(current_price, 4),
                    "change_24h": round(change, 2),
                    "volume_24h": f"{random.randint(100, 999)}M",
                    "last_updated": datetime.utcnow(),
                    "mode": "demo"
                })
        
        return market_data
    
    async def place_order(self, user_id: str, order_data: Dict) -> Dict:
        """Colocar orden (demo o real)"""
        if user_id not in self.connected_users:
            raise Exception("Usuario no conectado a Zaffex")
        
        credentials = self.connected_users[user_id]
        
        # Modo Demo
        if self._is_demo_credentials(credentials['api_key'], credentials['api_secret']):
            await asyncio.sleep(0.5)  # Simular latencia
            
            success_rate = 0.85
            if random.random() < success_rate:
                order_id = f"DEMO_{random.randint(100000, 999999)}"
                
                return {
                    "order_id": order_id,
                    "status": "FILLED",
                    "symbol": order_data["symbol"],
                    "type": order_data["type"],
                    "amount": order_data["amount"],
                    "price": order_data["price"], 
                    "total": order_data["amount"] * order_data["price"],
                    "executed_at": datetime.utcnow(),
                    "fees": round(order_data["amount"] * order_data["price"] * 0.001, 4),
                    "mode": "demo"
                }
            else:
                raise Exception("Error simulado en orden demo")
        
        # Modo Real - ⚠️ USA DINERO REAL
        try:
            timestamp = str(int(time.time() * 1000))
            
            params = {
                'symbol': order_data['symbol'].replace('/', ''),
                'side': order_data['type'].upper(),
                'type': 'MARKET',
                'quantity': f"{order_data['amount']:.8f}",
                'timestamp': timestamp
            }
            
            query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
            signature = self._generate_signature(credentials['api_secret'], query_string)
            
            headers = {
                'X-ZAFFEX-APIKEY': credentials['api_key'],
                'X-ZAFFEX-SIGNATURE': signature,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            logger.warning(f"⚠️ PLACING REAL ORDER: {params}")
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f"{self.base_url}/api/v3/order",
                    headers=headers,
                    data=params
                ) as response:
                    
                    result = await response.json()
                    
                    if response.status == 200:
                        return {
                            "order_id": result.get('orderId'),
                            "status": result.get('status', 'FILLED'),
                            "symbol": order_data['symbol'],
                            "type": order_data['type'],
                            "amount": float(result.get('executedQty', order_data['amount'])),
                            "price": float(result.get('price', order_data['price'])),
                            "total": float(result.get('cummulativeQuoteQty', 0)),
                            "executed_at": datetime.utcnow(),
                            "fees": float(result.get('fills', [{}])[0].get('commission', 0)) if result.get('fills') else 0,
                            "mode": "real"
                        }
                    else:
                        raise Exception(f"API Error: {result.get('msg', 'Unknown error')}")
                        
        except Exception as e:
            logger.error(f"Error placing real order: {e}")
            raise e
    
    async def get_order_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Obtener historial de órdenes"""
        if user_id not in self.connected_users:
            raise Exception("Usuario no conectado a Zaffex")
        
        credentials = self.connected_users[user_id]
        
        # Modo Demo
        if self._is_demo_credentials(credentials['api_key'], credentials['api_secret']):
            history = []
            symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT", "DOT/USDT"]
            
            for i in range(limit):
                symbol = random.choice(symbols)
                trade_type = random.choice(["BUY", "SELL"])
                amount = round(random.uniform(0.001, 1.0), 6)
                price = random.uniform(100, 50000)
                
                history.append({
                    "order_id": f"DEMO_{random.randint(100000, 999999)}",
                    "symbol": symbol,
                    "type": trade_type,
                    "amount": amount,
                    "price": round(price, 2),
                    "total": round(amount * price, 2),
                    "status": "FILLED",
                    "executed_at": datetime.utcnow(),
                    "profit_loss": round(random.uniform(-100, 200), 2),
                    "mode": "demo"
                })
            
            return history
        
        # Modo Real
        try:
            timestamp = str(int(time.time() * 1000))
            
            params = {
                'timestamp': timestamp,
                'limit': str(limit)
            }
            
            query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
            signature = self._generate_signature(credentials['api_secret'], query_string)
            
            headers = {
                'X-ZAFFEX-APIKEY': credentials['api_key'],
                'X-ZAFFEX-SIGNATURE': signature
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(
                    f"{self.base_url}/api/v3/allOrders",
                    headers=headers,
                    params=params
                ) as response:
                    
                    if response.status == 200:
                        orders = await response.json()
                        
                        processed_orders = []
                        for order in orders:
                            processed_orders.append({
                                "order_id": order.get('orderId'),
                                "symbol": order.get('symbol', '').replace('USDT', '/USDT'),
                                "type": order.get('side'),
                                "amount": float(order.get('executedQty', 0)),
                                "price": float(order.get('price', 0)),
                                "total": float(order.get('cummulativeQuoteQty', 0)),
                                "status": order.get('status'),
                                "executed_at": datetime.fromtimestamp(order.get('time', 0) / 1000),
                                "mode": "real"
                            })
                        
                        return processed_orders
                    else:
                        raise Exception(f"Error getting order history: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error getting real order history: {e}")
            return []
    
    def connect_user(self, user_id: str, api_key: str, api_secret: str):
        """Conectar usuario con sus credenciales"""
        self.connected_users[user_id] = {
            "api_key": api_key,
            "api_secret": api_secret,
            "connected_at": datetime.utcnow(),
            "mode": "demo" if self._is_demo_credentials(api_key, api_secret) else "real"
        }
        
        mode = "DEMO" if self._is_demo_credentials(api_key, api_secret) else "REAL"
        logger.info(f"User {user_id} connected to Zaffex in {mode} mode")
    
    def disconnect_user(self, user_id: str):
        """Desconectar usuario de Zaffex"""
        if user_id in self.connected_users:
            del self.connected_users[user_id]
            logger.info(f"User {user_id} disconnected from Zaffex")
    
    def is_user_connected(self, user_id: str) -> bool:
        """Verificar si un usuario está conectado"""
        return user_id in self.connected_users
    
    def get_user_mode(self, user_id: str) -> str:
        """Obtener el modo del usuario (demo o real)"""
        if user_id in self.connected_users:
            return self.connected_users[user_id].get('mode', 'demo')
        return 'demo'

# Instancia global del servicio de producción
production_zaffex_service = ProductionZaffexService()