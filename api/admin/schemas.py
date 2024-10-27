# schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None

class WishlistBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserWithWishlists(UserBase):
    id: int
    wishlists: List[WishlistBase] = []

    class Config:
        orm_mode = True

class WishlistCreate(BaseModel):
    name: str
    user_id: int

class WishlistUpdate(BaseModel):
    name: Optional[str] = None

class ProductBase(BaseModel):
    id: int
    name: str
    price: Optional[float] = None

    class Config:
        orm_mode = True

class DashboardMetrics(BaseModel):
    total_users: int
    active_wishlists: int
    top_products: List[str]
    # Add other metrics as needed
