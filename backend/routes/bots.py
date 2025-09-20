from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime
import asyncio
import random
import os
from pathlib import Path
from dotenv import load_dotenv

from models.bot import TradingBot, BotCreate, BotUpdate, BotResponse, BotStatus
from models.trade import Trade, TradeType, TradeStatus
from services.production_zaffex_service import production_zaffex_service as zaffex_service
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/api/bots", tags=["bots"])

# Simulamos un usuario autenticado
def get_current_user_id():
    return "user_123"  # En producción, esto vendría del JWT token

@router.post("/", response_model=BotResponse)
async def create_bot(bot_data: BotCreate, user_id: str = Depends(get_current_user_id)):
    """Crear un nuevo bot de trading"""
    
    bot = TradingBot(
        user_id=user_id,
        name=bot_data.name,
        strategy=bot_data.strategy,
        risk_level=bot_data.risk_level,
        initial_investment=bot_data.initial_investment,
        max_investment_per_trade=bot_data.max_investment_per_trade,
        stop_loss_percentage=bot_data.stop_loss_percentage,
        take_profit_percentage=bot_data.take_profit_percentage
    )
    
    # Guardar en MongoDB
    result = await db.bots.insert_one(bot.dict())
    
    if result.inserted_id:
        return BotResponse(**bot.dict())
    else:
        raise HTTPException(status_code=500, detail="Error al crear el bot")

@router.get("/", response_model=List[BotResponse])
async def get_user_bots(user_id: str = Depends(get_current_user_id)):
    """Obtener todos los bots del usuario"""
    
    bots_cursor = db.bots.find({"user_id": user_id})
    bots = await bots_cursor.to_list(length=None)
    
    return [BotResponse(**bot) for bot in bots]

@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: str, user_id: str = Depends(get_current_user_id)):
    """Obtener un bot específico"""
    
    bot = await db.bots.find_one({"id": bot_id, "user_id": user_id})
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot no encontrado")
    
    return BotResponse(**bot)

@router.put("/{bot_id}", response_model=BotResponse)
async def update_bot(bot_id: str, bot_update: BotUpdate, user_id: str = Depends(get_current_user_id)):
    """Actualizar configuración de un bot"""
    
    update_data = {k: v for k, v in bot_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.bots.update_one(
        {"id": bot_id, "user_id": user_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Bot no encontrado")
    
    updated_bot = await db.bots.find_one({"id": bot_id, "user_id": user_id})
    return BotResponse(**updated_bot)

@router.post("/{bot_id}/activate")
async def activate_bot(bot_id: str, user_id: str = Depends(get_current_user_id)):
    """Activar un bot de trading"""
    
    bot = await db.bots.find_one({"id": bot_id, "user_id": user_id})
    if not bot:
        raise HTTPException(status_code=404, detail="Bot no encontrado")
    
    # Verificar conexión con Zaffex
    if not zaffex_service.is_user_connected(user_id):
        raise HTTPException(
            status_code=400, 
            detail="Debes conectar tu cuenta de Zaffex antes de activar bots"
        )
    
    # Activar bot
    await db.bots.update_one(
        {"id": bot_id, "user_id": user_id},
        {"$set": {
            "is_active": True,
            "status": BotStatus.ACTIVE.value,
            "updated_at": datetime.utcnow()
        }}
    )
    
    # Iniciar trading en background (simulado)
    asyncio.create_task(start_trading_loop(bot_id, user_id))
    
    return {"message": "Bot activado exitosamente"}

@router.post("/{bot_id}/deactivate")
async def deactivate_bot(bot_id: str, user_id: str = Depends(get_current_user_id)):
    """Desactivar un bot de trading"""
    
    await db.bots.update_one(
        {"id": bot_id, "user_id": user_id},
        {"$set": {
            "is_active": False,
            "status": BotStatus.INACTIVE.value,
            "updated_at": datetime.utcnow()
        }}
    )
    
    return {"message": "Bot desactivado exitosamente"}

@router.delete("/{bot_id}")
async def delete_bot(bot_id: str, user_id: str = Depends(get_current_user_id)):
    """Eliminar un bot"""
    
    # Primero desactivar si está activo
    await deactivate_bot(bot_id, user_id)
    
    result = await db.bots.delete_one({"id": bot_id, "user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bot no encontrado")
    
    return {"message": "Bot eliminado exitosamente"}

@router.get("/{bot_id}/performance")
async def get_bot_performance(bot_id: str, user_id: str = Depends(get_current_user_id)):
    """Obtener métricas de rendimiento de un bot"""
    
    bot = await db.bots.find_one({"id": bot_id, "user_id": user_id})
    if not bot:
        raise HTTPException(status_code=404, detail="Bot no encontrado")
    
    # Obtener trades del bot
    trades_cursor = db.trades.find({"bot_id": bot_id}).sort("created_at", -1)
    trades = await trades_cursor.to_list(length=50)
    
    # Calcular métricas
    total_trades = len(trades)
    successful_trades = len([t for t in trades if t.get("profit_loss", 0) > 0])
    total_profit = sum([t.get("profit_loss", 0) for t in trades])
    
    return {
        "bot_id": bot_id,
        "total_trades": total_trades,
        "successful_trades": successful_trades,
        "accuracy": (successful_trades / total_trades * 100) if total_trades > 0 else 0,
        "total_profit": total_profit,
        "roi": (total_profit / bot["initial_investment"] * 100) if bot["initial_investment"] > 0 else 0,
        "recent_trades": trades[:10]
    }

async def start_trading_loop(bot_id: str, user_id: str):
    """Bucle de trading simulado para un bot activo"""
    
    while True:
        try:
            # Verificar si el bot sigue activo
            bot = await db.bots.find_one({"id": bot_id, "user_id": user_id})
            if not bot or not bot.get("is_active", False):
                break
            
            # Simular análisis de mercado y decisión de trading
            should_trade = random.random() < 0.3  # 30% probabilidad de hacer trade
            
            if should_trade:
                await simulate_trade(bot_id, user_id, bot)
            
            # Esperar antes del próximo ciclo (entre 30 segundos y 5 minutos)
            await asyncio.sleep(random.randint(30, 300))
            
        except Exception as e:
            print(f"Error en trading loop para bot {bot_id}: {e}")
            # En caso de error, pausar el bot
            await db.bots.update_one(
                {"id": bot_id},
                {"$set": {"status": BotStatus.ERROR.value}}
            )
            break

async def simulate_trade(bot_id: str, user_id: str, bot: dict):
    """Simula la ejecución de un trade"""
    
    # Seleccionar par de trading aleatorio
    trading_pairs = ["BTC/USDT", "ETH/USDT", "ADA/USDT", "DOT/USDT"]
    pair = random.choice(trading_pairs)
    
    # Obtener precio actual del mercado
    market_data = await zaffex_service.get_market_data([pair])
    if not market_data:
        return
    
    current_price = market_data[0]["price"]
    trade_type = random.choice([TradeType.BUY, TradeType.SELL])
    
    # Calcular cantidad basada en la configuración del bot
    max_investment = bot.get("max_investment_per_trade", 100)
    amount = random.uniform(max_investment * 0.1, max_investment) / current_price
    
    try:
        # Intentar ejecutar orden en Zaffex
        order_result = await zaffex_service.place_order(user_id, {
            "symbol": pair,
            "type": trade_type.value,
            "amount": amount,
            "price": current_price
        })
        
        # Simular profit/loss
        profit_factor = random.uniform(-0.05, 0.15)  # Entre -5% y +15%
        profit_loss = amount * current_price * profit_factor
        
        # Crear registro de trade
        trade = Trade(
            bot_id=bot_id,
            user_id=user_id,
            trading_pair=pair,
            trade_type=trade_type,
            amount=amount,
            price=current_price,
            total_value=amount * current_price,
            profit_loss=profit_loss,
            profit_percentage=profit_factor * 100,
            status=TradeStatus.EXECUTED,
            executed_at=datetime.utcnow(),
            zaffex_order_id=order_result["order_id"],
            strategy_used=bot["strategy"]
        )
        
        # Guardar trade en BD
        await db.trades.insert_one(trade.dict())
        
        # Actualizar estadísticas del bot
        await update_bot_statistics(bot_id, profit_loss)
        
        print(f"Trade ejecutado: {trade_type.value} {amount:.6f} {pair} a ${current_price:.2f} - P/L: ${profit_loss:.2f}")
        
    except Exception as e:
        print(f"Error al ejecutar trade: {e}")

async def update_bot_statistics(bot_id: str, profit_loss: float):
    """Actualiza las estadísticas de rendimiento del bot"""
    
    bot = await db.bots.find_one({"id": bot_id})
    if not bot:
        return
    
    # Actualizar métricas
    new_profit = bot.get("profit", 0) + profit_loss
    new_total_trades = bot.get("total_trades", 0) + 1
    new_successful_trades = bot.get("successful_trades", 0) + (1 if profit_loss > 0 else 0)
    new_accuracy = (new_successful_trades / new_total_trades * 100) if new_total_trades > 0 else 0
    new_roi = (new_profit / bot["initial_investment"] * 100) if bot["initial_investment"] > 0 else 0
    
    await db.bots.update_one(
        {"id": bot_id},
        {"$set": {
            "profit": new_profit,
            "total_trades": new_total_trades,
            "successful_trades": new_successful_trades,
            "accuracy": new_accuracy,
            "roi": new_roi,
            "last_trade_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }}
    )