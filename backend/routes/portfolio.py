from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timedelta
import asyncio

from models.portfolio import Portfolio, PortfolioResponse, AssetHolding, MarketData
from services.zaffex_service import zaffex_service
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

def get_current_user_id():
    return "user_123"  # En producción, esto vendría del JWT token

@router.get("/", response_model=PortfolioResponse)
async def get_portfolio(user_id: str = Depends(get_current_user_id)):
    """Obtener el portfolio completo del usuario"""
    
    # Buscar portfolio existente
    portfolio = await db.portfolios.find_one({"user_id": user_id})
    
    if not portfolio:
        # Crear portfolio inicial si no existe
        initial_portfolio = Portfolio(
            user_id=user_id,
            total_balance=40000.0,
            available_balance=35000.0,
            in_orders=5000.0,
            initial_investment=40000.0
        )
        await db.portfolios.insert_one(initial_portfolio.dict())
        portfolio = initial_portfolio.dict()
    
    # Actualizar con datos en tiempo real si hay conexión con Zaffex
    if zaffex_service.is_user_connected(user_id):
        try:
            balance_info = await zaffex_service.get_account_balance(user_id)
            
            # Actualizar balances
            portfolio["total_balance"] = balance_info["total_balance"]
            portfolio["available_balance"] = balance_info["available_balance"] 
            portfolio["in_orders"] = balance_info["in_orders"]
            
            # Calcular métricas de rendimiento
            portfolio["total_profit_loss"] = portfolio["total_balance"] - portfolio["initial_investment"]
            portfolio["total_profit_percentage"] = (portfolio["total_profit_loss"] / portfolio["initial_investment"]) * 100
            
            # Actualizar en base de datos
            await db.portfolios.update_one(
                {"user_id": user_id},
                {"$set": portfolio}
            )
            
        except Exception as e:
            print(f"Error actualizando portfolio desde Zaffex: {e}")
    
    return PortfolioResponse(**portfolio)

@router.get("/holdings", response_model=List[AssetHolding])
async def get_asset_holdings(user_id: str = Depends(get_current_user_id)):
    """Obtener las tenencias de activos del usuario"""
    
    # Obtener trades recientes para calcular holdings
    trades_cursor = db.trades.find({"user_id": user_id, "status": "executed"})
    trades = await trades_cursor.to_list(length=None)
    
    # Agrupar por activo
    holdings_dict = {}
    
    for trade in trades:
        symbol = trade["trading_pair"].split("/")[0]  # BTC de BTC/USDT
        
        if symbol not in holdings_dict:
            holdings_dict[symbol] = {
                "symbol": symbol,
                "amount": 0.0,
                "total_cost": 0.0,
                "trades": 0
            }
        
        if trade["trade_type"] == "BUY":
            holdings_dict[symbol]["amount"] += trade["amount"]
            holdings_dict[symbol]["total_cost"] += trade["total_value"]
        else:  # SELL
            holdings_dict[symbol]["amount"] -= trade["amount"]
            holdings_dict[symbol]["total_cost"] -= trade["total_value"]
        
        holdings_dict[symbol]["trades"] += 1
    
    # Obtener precios actuales
    symbols = [f"{symbol}/USDT" for symbol in holdings_dict.keys()]
    market_data = await zaffex_service.get_market_data(symbols) if symbols else []
    
    # Crear objetos AssetHolding
    holdings = []
    for symbol, data in holdings_dict.items():
        if data["amount"] > 0:  # Solo mostrar activos con balance positivo
            # Buscar precio actual
            current_price = 0
            for market in market_data:
                if market["symbol"] == f"{symbol}/USDT":
                    current_price = market["price"]
                    break
            
            average_price = data["total_cost"] / data["amount"] if data["amount"] > 0 else 0
            total_value = data["amount"] * current_price
            profit_loss = total_value - (data["amount"] * average_price)
            profit_percentage = (profit_loss / (data["amount"] * average_price)) * 100 if average_price > 0 else 0
            
            holding = AssetHolding(
                symbol=symbol,
                amount=data["amount"],
                average_price=average_price,
                current_price=current_price,
                total_value=total_value,
                profit_loss=profit_loss,
                profit_percentage=profit_percentage
            )
            holdings.append(holding)
    
    return holdings

@router.get("/performance")
async def get_portfolio_performance(
    period: str = "7d",  # 1d, 7d, 30d, 1y
    user_id: str = Depends(get_current_user_id)
):
    """Obtener métricas de rendimiento del portfolio"""
    
    # Definir rango de fechas
    now = datetime.utcnow()
    if period == "1d":
        start_date = now - timedelta(days=1)
    elif period == "7d":
        start_date = now - timedelta(days=7)
    elif period == "30d":
        start_date = now - timedelta(days=30)
    elif period == "1y":
        start_date = now - timedelta(days=365)
    else:
        start_date = now - timedelta(days=7)
    
    # Obtener trades del período
    trades_cursor = db.trades.find({
        "user_id": user_id,
        "executed_at": {"$gte": start_date},
        "status": "executed"
    }).sort("executed_at", 1)
    
    trades = await trades_cursor.to_list(length=None)
    
    # Calcular métricas
    total_trades = len(trades)
    profitable_trades = len([t for t in trades if t.get("profit_loss", 0) > 0])
    total_profit_loss = sum([t.get("profit_loss", 0) for t in trades])
    total_volume = sum([t.get("total_value", 0) for t in trades])
    
    # Agrupar por día para gráfico
    daily_performance = {}
    for trade in trades:
        date_key = trade["executed_at"].strftime("%Y-%m-%d")
        if date_key not in daily_performance:
            daily_performance[date_key] = {
                "date": date_key,
                "profit_loss": 0,
                "trades": 0,
                "volume": 0
            }
        
        daily_performance[date_key]["profit_loss"] += trade.get("profit_loss", 0)
        daily_performance[date_key]["trades"] += 1
        daily_performance[date_key]["volume"] += trade.get("total_value", 0)
    
    # Obtener portfolio actual
    portfolio = await get_portfolio(user_id)
    
    return {
        "period": period,
        "summary": {
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "win_rate": (profitable_trades / total_trades * 100) if total_trades > 0 else 0,
            "total_profit_loss": total_profit_loss,
            "total_volume": total_volume,
            "current_balance": portfolio.total_balance,
            "roi": portfolio.total_profit_percentage
        },
        "daily_data": list(daily_performance.values()),
        "top_performing_assets": await get_top_performing_assets(user_id, start_date),
        "recent_trades": trades[-10:] if trades else []
    }

async def get_top_performing_assets(user_id: str, start_date: datetime):
    """Obtener los activos con mejor rendimiento"""
    
    # Obtener trades del período agrupados por activo
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "executed_at": {"$gte": start_date},
                "status": "executed"
            }
        },
        {
            "$group": {
                "_id": "$trading_pair",
                "total_profit_loss": {"$sum": "$profit_loss"},
                "total_trades": {"$sum": 1},
                "total_volume": {"$sum": "$total_value"}
            }
        },
        {
            "$sort": {"total_profit_loss": -1}
        },
        {
            "$limit": 5
        }
    ]
    
    cursor = db.trades.aggregate(pipeline)
    results = await cursor.to_list(length=None)
    
    return [
        {
            "asset": result["_id"],
            "profit_loss": result["total_profit_loss"],
            "trades": result["total_trades"],
            "volume": result["total_volume"]
        }
        for result in results
    ]

@router.post("/sync")
async def sync_portfolio_with_zaffex(user_id: str = Depends(get_current_user_id)):
    """Sincronizar portfolio con datos de Zaffex"""
    
    if not zaffex_service.is_user_connected(user_id):
        raise HTTPException(
            status_code=400,
            detail="No hay conexión activa con Zaffex"
        )
    
    try:
        # Obtener datos actualizados de Zaffex
        balance_info = await zaffex_service.get_account_balance(user_id)
        order_history = await zaffex_service.get_order_history(user_id, limit=100)
        
        # Actualizar portfolio
        portfolio = await db.portfolios.find_one({"user_id": user_id})
        if not portfolio:
            portfolio = Portfolio(user_id=user_id).dict()
        
        # Actualizar balances
        portfolio["total_balance"] = balance_info["total_balance"]
        portfolio["available_balance"] = balance_info["available_balance"]
        portfolio["in_orders"] = balance_info["in_orders"]
        
        # Calcular métricas actualizadas
        portfolio["total_profit_loss"] = portfolio["total_balance"] - portfolio["initial_investment"]
        portfolio["total_profit_percentage"] = (portfolio["total_profit_loss"] / portfolio["initial_investment"]) * 100
        portfolio["updated_at"] = datetime.utcnow()
        
        # Guardar cambios
        await db.portfolios.update_one(
            {"user_id": user_id},
            {"$set": portfolio},
            upsert=True
        )
        
        return {
            "message": "Portfolio sincronizado exitosamente",
            "balance_info": balance_info,
            "orders_imported": len(order_history),
            "sync_time": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al sincronizar portfolio: {str(e)}"
        )