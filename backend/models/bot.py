from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class RiskLevel(str, Enum):
    LOW = "Bajo"
    MEDIUM = "Medio" 
    HIGH = "Alto"

class BotStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"
    ERROR = "error"

class Strategy(str, Enum):
    GRID_TRADING = "Grid Trading"
    DCA_RSI = "DCA + RSI"
    MOMENTUM_TRADING = "Momentum Trading"
    HIGH_FREQUENCY = "High Frequency"
    CROSS_EXCHANGE = "Cross Exchange"
    MACHINE_LEARNING = "Machine Learning"

class TradingBot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    strategy: Strategy
    risk_level: RiskLevel
    is_active: bool = False
    status: BotStatus = BotStatus.INACTIVE
    
    # Performance metrics
    profit: float = 0.0
    roi: float = 0.0
    accuracy: float = 0.0
    total_trades: int = 0
    successful_trades: int = 0
    
    # Configuration
    initial_investment: float
    max_investment_per_trade: float = 100.0
    stop_loss_percentage: float = 5.0
    take_profit_percentage: float = 10.0
    
    # Zaffex connection
    zaffex_api_key: Optional[str] = None
    zaffex_secret: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_trade_at: Optional[datetime] = None

class BotCreate(BaseModel):
    name: str
    strategy: Strategy
    risk_level: RiskLevel
    initial_investment: float
    max_investment_per_trade: float = 100.0
    stop_loss_percentage: float = 5.0
    take_profit_percentage: float = 10.0

class BotUpdate(BaseModel):
    name: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    max_investment_per_trade: Optional[float] = None
    stop_loss_percentage: Optional[float] = None
    take_profit_percentage: Optional[float] = None
    is_active: Optional[bool] = None

class BotResponse(BaseModel):
    id: str
    name: str
    strategy: Strategy
    risk_level: RiskLevel
    is_active: bool
    status: BotStatus
    profit: float
    roi: float
    accuracy: float
    total_trades: int
    successful_trades: int
    created_at: datetime
    last_trade_at: Optional[datetime] = None