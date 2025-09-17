from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from enum import Enum
import uuid

class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class TradeStatus(str, Enum):
    PENDING = "pending"
    EXECUTED = "executed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class Trade(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    bot_id: str
    user_id: str
    
    # Trade details
    trading_pair: str  # e.g., "BTC/USDT"
    trade_type: TradeType
    amount: float
    price: float
    total_value: float
    
    # Profit/Loss
    profit_loss: float = 0.0
    profit_percentage: float = 0.0
    
    # Status and execution
    status: TradeStatus = TradeStatus.PENDING
    executed_at: Optional[datetime] = None
    
    # Zaffex integration
    zaffex_order_id: Optional[str] = None
    
    # Metadata
    strategy_used: str
    market_conditions: Optional[Dict] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TradeCreate(BaseModel):
    bot_id: str
    trading_pair: str
    trade_type: TradeType
    amount: float
    price: float

class TradeResponse(BaseModel):
    id: str
    bot_id: str
    trading_pair: str
    trade_type: TradeType
    amount: float
    price: float
    total_value: float
    profit_loss: float
    profit_percentage: float
    status: TradeStatus
    executed_at: Optional[datetime] = None
    created_at: datetime