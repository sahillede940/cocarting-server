import json
from fastapi import FastAPI, Request, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from DB.models import Product, Wishlist, WishlistProduct, ProductImage
from DB.schemas import  AddToWishlist, CreateWishlistBase
from DB.database import engine, get_db, Base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import requests
from dotenv import load_dotenv
import os
from BackgroundMonitoring import scrape_product_data
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import asyncio
from sqlalchemy import func
from io import BytesIO
import pandas as pd
from fastapi.responses import StreamingResponse

load_dotenv()

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck")
def healthcheck(request: Request):
    return {
        "message": " Server is up and running",
        "domain": request.url.hostname,
    }


@app.get("/product")
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(Product).limit(10).all()
        return users
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

@app.get("/create_wishlist")
def create_wishlist(data: CreateWishlistBase, db: Session = Depends(get_db)):
    try:
        new_wishlist = Wishlist(
            name=data.name
        )
        db.save(new_wishlist)
        db.commit()
        return {"message": "Wishlist created successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e), "message": "Failed to create wishlist"}
    except Exception as e:
        db.rollback()
        return {"error": str(e), "message": "Failed to create wishlist"}


@app.post("/add_to_wishlist")
def add_to_wishlist(data: AddToWishlist, db: Session = Depends(get_db)):
    try:
        new_product = Product(
            name=data.product.name,
            original_price=data.product.original_price,
            customer_rating=data.product.customer_rating,
            price=data.product.price,
            product_source=data.product.product_source,
        )
        db.save(new_product)
        db.commit()
        new_wishlist = Wishlist(
            id=data.wishlist.id
        )
        db.save(new_wishlist)
        db.commit()
        new_wishlist_product = WishlistProduct(
            product_id=new_product.id,
            wishlist_id=new_wishlist.id
        )
        db.save(new_wishlist_product)
        db.commit()
        return {"message": "Product added to wishlist successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e), "message": "Failed to add product to wishlist"}
    except Exception as e:
        db.rollback()
        return {"error": str(e), "message": "Failed to add product to wishlist"}