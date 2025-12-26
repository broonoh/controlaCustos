from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- Esquemas de Usuário (NOVO) ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Esquemas de Autenticação (NOVO) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Seus Esquemas de Categoria (MANTIDOS) ---
class CategoryBase(BaseModel):
    name: str
    color: Optional[str] = "#3498db"

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- Seus Esquemas de Transação (MANTIDOS) ---
class TransactionBase(BaseModel):
    description: str
    amount: float
    type: str 
    category_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime
    class Config:
        from_attributes = True