from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from DB.database import get_db
from DB.models import User, Wishlist, WishlistProduct, Product

from sqlalchemy import func, desc

admin_router = APIRouter(prefix="/admin", tags=["Admin"])



# Pydantic Schemas


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class WishlistBase(BaseModel):
    name: str


class WishlistCreate(WishlistBase):
    pass


class WishlistOut(WishlistBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    id: int
    name: str
    price: Optional[float]

    class Config:
        orm_mode = True

# Admin Endpoints

# User Management


@admin_router.get("/users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@admin_router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@admin_router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = user_update.email
    db.commit()
    db.refresh(user)
    return user


@admin_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

# Wishlist Monitoring


@admin_router.get("/wishlists", response_model=List[WishlistOut])
def get_all_wishlists(db: Session = Depends(get_db)):
    wishlists = db.query(Wishlist).all()
    return wishlists


@admin_router.get("/wishlists/{wishlist_id}", response_model=WishlistOut)
def get_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
    wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist is None:
        raise HTTPException(status_code=404, detail="Wishlist not found")
    return wishlist

# Reports on Popular Products and WishLists

@admin_router.get("/reports/popular-wishlists", response_model=List[WishlistOut])
def get_popular_wishlists(limit: int = 10, db: Session = Depends(get_db)):
    popular_wishlists = (
        db.query(Wishlist, func.count(
            WishlistProduct.wishlist_id).label('count'))
        .join(WishlistProduct, Wishlist.id == WishlistProduct.wishlist_id)
        .group_by(Wishlist.id)
        .order_by(desc('count'))
        .limit(limit)
        .all()
    )
    return popular_wishlists
