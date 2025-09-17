from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class AssetHolding(BaseModel):
    symbol: str  # e.g., "BTC", "ETH", "USDT"
    amount: float
    average_price: float
    current_price: float
    total_value: float
    profit_loss: float
    profit_percentage: float

class Portfolio(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Balance information
    total_balance: float = 0.0
    available_balance: float = 0.0
    in_orders: float = 0.0
    initial_investment: float = 0.0
    
    # Performance metrics
    total_profit_loss: float = 0.0
    total_profit_percentage: float = 0.0
    daily_profit_loss: float = 0.0
    daily_profit_percentage: float = 0.0
    
    # Asset holdings
    holdings: List[AssetHolding] = []
    
    # Statistics
    total_trades: int = 0
    successful_trades: int = 0
    accuracy: float = 0.0
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PortfolioResponse(BaseModel):
    id: str
    user_id: str
    total_balance: float
    available_balance: float
    in_orders: float
    initial_investment: float
    total_profit_loss: float
    total_profit_percentage: float
    daily_profit_loss: float
    daily_profit_percentage: float
    holdings: List[AssetHolding]
    total_trades: int
    successful_trades: int
    accuracy: float
    updated_at: datetime

class MarketData(BaseModel):
    symbol: str
    price: float
    change_24h: float
    change_percentage_24h: float
    volume_24h: str
    market_cap: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)