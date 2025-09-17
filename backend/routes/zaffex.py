from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, List
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

from models.user import ZaffexConnectionUpdate
from services.zaffex_service import zaffex_service
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/api/zaffex", tags=["zaffex"])

def get_current_user_id():
    return "user_123"  # En producción, esto vendría del JWT token

@router.post("/connect")
async def connect_zaffex(
    connection_data: ZaffexConnectionUpdate, 
    user_id: str = Depends(get_current_user_id)
):
    """Conectar cuenta de Zaffex con credenciales API"""
    
    try:
        # Validar credenciales con Zaffex
        is_valid = await zaffex_service.validate_credentials(
            connection_data.api_key, 
            connection_data.api_secret
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=400, 
                detail="Credenciales de Zaffex inválidas"
            )
        
        # Conectar usuario al servicio
        zaffex_service.connect_user(
            user_id, 
            connection_data.api_key, 
            connection_data.api_secret
        )
        
        # Obtener balance inicial
        balance_info = await zaffex_service.get_account_balance(user_id)
        
        # Actualizar información en la base de datos
        await db.users.update_one(
            {"id": user_id},
            {"$set": {
                "zaffex_connection.api_key": connection_data.api_key,
                "zaffex_connection.api_secret": connection_data.api_secret,
                "zaffex_connection.is_connected": True,
                "zaffex_connection.test_mode": connection_data.test_mode,
                "zaffex_connection.last_sync": datetime.utcnow(),
                "zaffex_connection.balance": balance_info["total_balance"],
                "updated_at": datetime.utcnow()
            }},
            upsert=True
        )
        
        return {
            "message": "Conexión con Zaffex exitosa",
            "balance_info": balance_info,
            "test_mode": connection_data.test_mode
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con Zaffex: {str(e)}")

@router.delete("/disconnect")
async def disconnect_zaffex(user_id: str = Depends(get_current_user_id)):
    """Desconectar cuenta de Zaffex"""
    
    # Desconectar del servicio
    zaffex_service.disconnect_user(user_id)
    
    # Actualizar base de datos
    await db.users.update_one(
        {"id": user_id},
        {"$set": {
            "zaffex_connection.api_key": None,
            "zaffex_connection.api_secret": None,
            "zaffex_connection.is_connected": False,
            "zaffex_connection.last_sync": None,
            "zaffex_connection.balance": 0.0,
            "updated_at": datetime.utcnow()
        }}
    )
    
    return {"message": "Desconectado de Zaffex exitosamente"}

@router.get("/status")
async def get_zaffex_status(user_id: str = Depends(get_current_user_id)):
    """Obtener estado de la conexión con Zaffex"""
    
    user = await db.users.find_one({"id": user_id})
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    connection = user.get("zaffex_connection", {})
    is_connected = zaffex_service.is_user_connected(user_id)
    
    return {
        "is_connected": is_connected,
        "test_mode": connection.get("test_mode", True),
        "last_sync": connection.get("last_sync"),
        "balance": connection.get("balance", 0.0),
        "has_credentials": bool(connection.get("api_key"))
    }

@router.get("/balance")
async def get_zaffex_balance(user_id: str = Depends(get_current_user_id)):
    """Obtener balance actual de Zaffex"""
    
    if not zaffex_service.is_user_connected(user_id):
        raise HTTPException(
            status_code=400, 
            detail="No hay conexión activa con Zaffex"
        )
    
    try:
        balance_info = await zaffex_service.get_account_balance(user_id)
        
        # Actualizar balance en la base de datos
        await db.users.update_one(
            {"id": user_id},
            {"$set": {
                "zaffex_connection.balance": balance_info["total_balance"],
                "zaffex_connection.last_sync": datetime.utcnow()
            }}
        )
        
        return balance_info
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener balance de Zaffex: {str(e)}"
        )

@router.get("/market-data")
async def get_market_data(symbols: str = "BTC/USDT,ETH/USDT,ADA/USDT,DOT/USDT"):
    """Obtener datos de mercado en tiempo real"""
    
    symbol_list = [s.strip() for s in symbols.split(",")]
    
    try:
        market_data = await zaffex_service.get_market_data(symbol_list)
        return {"data": market_data}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener datos de mercado: {str(e)}"
        )

@router.get("/order-history")
async def get_order_history(
    limit: int = 50, 
    user_id: str = Depends(get_current_user_id)
):
    """Obtener historial de órdenes de Zaffex"""
    
    if not zaffex_service.is_user_connected(user_id):
        raise HTTPException(
            status_code=400, 
            detail="No hay conexión activa con Zaffex"
        )
    
    try:
        history = await zaffex_service.get_order_history(user_id, limit)
        return {"orders": history}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener historial: {str(e)}"
        )

@router.post("/test-connection")
async def test_zaffex_connection(user_id: str = Depends(get_current_user_id)):
    """Probar la conexión con Zaffex"""
    
    if not zaffex_service.is_user_connected(user_id):
        raise HTTPException(
            status_code=400, 
            detail="No hay conexión activa con Zaffex"
        )
    
    try:
        # Probar obtener balance
        balance_info = await zaffex_service.get_account_balance(user_id)
        
        # Probar obtener datos de mercado
        market_data = await zaffex_service.get_market_data(["BTC/USDT"])
        
        return {
            "status": "success",
            "message": "Conexión con Zaffex funcionando correctamente",
            "balance": balance_info,
            "market_data_available": len(market_data) > 0,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error en la conexión: {str(e)}",
            "timestamp": datetime.utcnow()
        }