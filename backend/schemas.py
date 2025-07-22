from pydantic import BaseModel
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    student_id: Optional[str] = None
    class_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    usage_count: Optional[int] = None
    password: Optional[str] = None
    name: Optional[str] = None
    student_id: Optional[str] = None
    class_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    usage_count: int
    created_at: datetime.datetime
    is_active: bool
    name: Optional[str] = None
    student_id: Optional[str] = None
    class_name: Optional[str] = None
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    out_trade_no: str
    amount: float
    remark: Optional[str] = None

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str

class AdminOut(AdminBase):
    id: int
    class Config:
        orm_mode = True 