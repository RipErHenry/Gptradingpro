from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict
from datetime import datetime
import uuid

class ZaffexConnection(BaseModel):
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    is_connected: bool = False
    test_mode: bool = True
    last_sync: Optional[datetime] = None
    balance: float = 0.0

class NotificationSettings(BaseModel):
    trades: bool = True
    profits: bool = True
    losses: bool = True
    bot_status: bool = True
    email: bool = False
    telegram: bool = False

class SecuritySettings(BaseModel):
    two_factor_enabled: bool = False
    max_trade_amount: float = 1000.0
    daily_trade_limit: float = 10000.0

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    hashed_password: str
    
    # Profile
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timezone: str = "UTC"
    
    # Trading configuration
    zaffex_connection: ZaffexConnection = Field(default_factory=ZaffexConnection)
    notification_settings: NotificationSettings = Field(default_factory=NotificationSettings)
    security_settings: SecuritySettings = Field(default_factory=SecuritySettings)
    
    # Account status
    is_active: bool = True
    is_verified: bool = False
    subscription_tier: str = "free"  # free, standard, premium
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timezone: str
    is_active: bool
    is_verified: bool
    subscription_tier: str
    created_at: datetime
    last_login: Optional[datetime] = None

class ZaffexConnectionUpdate(BaseModel):
    api_key: str
    api_secret: str
    test_mode: bool = True