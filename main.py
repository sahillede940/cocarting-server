import json
from fastapi import FastAPI, Request, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from DB.models import Product
from DB.schemas import ProductBase, WishlistBase, UpdateProductBase
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