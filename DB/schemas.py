from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas


class UserCreate(BaseModel):
    email: EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    wishlists: List['Wishlist'] = []

    class Config:
        orm_mode = True


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

# Product schemas


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

# Wishlist schemas


class WishlistCreate(BaseModel):
    name: str
    user_id: int


class Wishlist(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    products: List['WishlistProduct'] = []

    class Config:
        orm_mode = True

# WishlistProduct schemas


class WishlistProductCreate(BaseModel):
    wishlist_id: int
    product: ProductCreate
    note: Optional[str] = None


class WishlistProduct(BaseModel):
    id: int
    wishlist_id: int
    product_id: int
    note: Optional[str] = None

    class Config:
        orm_mode = True

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