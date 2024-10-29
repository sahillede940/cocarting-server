from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas

class UserCreate(BaseModel):
    email: EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    cocarts: List['Cocart'] = []

    class Config:
        orm_mode = True

# Product schemas

class ProductCreate(BaseModel):
    name: str
    original_price: Optional[float] = None
    price: Optional[float] = None
    customer_rating: Optional[str] = None
    product_tracking_url: Optional[str] = None
    slug: str
    added_by: Optional[int] = None
    image: Optional[str] = None

# Product Image schemas

class ProductImageBase(BaseModel):
    id: int
    product_id: int
    image: Optional[str] = None

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    id: int
    name: str
    original_price: Optional[float] = None
    price: Optional[float] = None
    customer_rating: Optional[str] = None
    added_by: Optional[int] = None
    product_tracking_url: Optional[str] = None
    image: ProductImageBase

    class Config:
        orm_mode = True

# Cocart schemas

class CocartCreate(BaseModel):
    name: str
    user_id: int

class Cocart(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    products: List['CocartProduct'] = []

    class Config:
        orm_mode = True

# CocartProduct schemas

class CocartProductCreate(BaseModel):
    cocart_id: int
    product: ProductCreate
    note: Optional[str] = None

class CocartProduct(BaseModel):
    id: int
    cocart_id: int
    product_id: int
    note: Optional[str] = None

    class Config:
        orm_mode = True

# Update Product schema

class UpdateProductBase(BaseModel):
    name: str
    original_price: Optional[float] = None
    price: Optional[float] = None
    customer_rating: Optional[str] = None
    product_tracking_url: Optional[str] = None
    image: ProductImageBase
    slug: str

    class Config:
        orm_mode = True
