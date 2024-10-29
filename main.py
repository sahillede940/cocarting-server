from fastapi import FastAPI, Request, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List

from DB.models import User, Cocart, Product, CocartProduct, ProductImage
from DB.schemas import (
    UserCreate, User as UserSchema,
    CocartCreate, Cocart as CocartSchema,
    CocartProductCreate, UpdateProductBase
)
from DB.database import engine, get_db, Base
from sqlalchemy.orm import joinedload
import requests
import os
from BackgroundMonitoring import scrape_product_data
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from api.admin.admin import admin_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(admin_router)

# CORS Middleware settings
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
        "message": "Server is up and running",
        "domain": request.url.hostname,
    }


async def monitor_product(db: Session):
    print(f"Scraping data at {datetime.now()}")
    await scrape(db)


def run_async_task():
    db = next(get_db())
    asyncio.run(monitor_product(db))


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_async_task, 'interval', days=7)
    scheduler.start()


@app.on_event("startup")
async def startup_event():
    start_scheduler()


def update_product(product_id: int, product: UpdateProductBase, db: Session):
    try:
        db.query(Product).filter_by(id=product_id).update(
            {
                "name": product.get("name"),
                "original_price": product.get("original_price"),
                "price": product.get("price"),
                "customer_rating": product.get("customer_rating"),
                "product_tracking_url": product.get("product_tracking_url"),
                "slug": product.get("slug"),
            }
        )

        if product.image:
            db.query(ProductImage).filter_by(product_id=product_id).update(
                {
                    "image": product.image
                }
            )

        db.commit()
        return {"message": "Product updated successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/monitor-product")
async def scrape(db: Session = Depends(get_db)):
    key = os.getenv("SCRAPER_API")
    url = f"https://api.scraperapi.com?api_key={key}&url="

    products = db.query(Product).all()
    for product in products:
        product_url = product.product_tracking_url
        product_id = product.id
        response = requests.get(url + product_url)
        product = await scrape_product_data(response.text, product_url)
        print(product)
        update_product(product_id, product, db)
        print("Product data updated successfully for product_id: ", product_id)

    return {"message": "Product data updated successfully"}


# User Endpoints

@app.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(
            User.email == user_create.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        new_user = User(email=user_create.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Cocart Endpoints

@app.post("/cocarts", response_model=CocartSchema, status_code=status.HTTP_201_CREATED)
def create_cocart(cocart_create: CocartCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(
            User.id == cocart_create.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        new_cocart = Cocart(
            name=cocart_create.name,
            user_id=cocart_create.user_id,
            slug=cocart_create.slug,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_cocart)
        db.commit()
        db.refresh(new_cocart)
        return new_cocart
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/cocarts/{user_id}", response_model=List[CocartSchema])
def get_cocarts(user_id: int, db: Session = Depends(get_db)):
    try:
        cocarts = db.query(Cocart).filter(
            Cocart.user_id == user_id).all()
        return cocarts
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.delete("/cocarts/{cocart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cocart(cocart_id: int, db: Session = Depends(get_db)):
    try:
        db.query(CocartProduct).filter(
            CocartProduct.cocart_id == cocart_id).delete()
        db.commit()

        cocart = db.query(Cocart).filter(
            Cocart.id == cocart_id).first()
        if not cocart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cocart not found"
            )
        db.delete(cocart)
        db.commit()

        return {"message": "Cocart deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Product Endpoints

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        db.delete(product)
        db.commit()

        cocart_product = db.query(CocartProduct).filter(
            CocartProduct.product_id == product_id).first()
        if cocart_product:
            db.delete(cocart_product)
            db.commit()

        return {"message": "Product deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# CocartProduct Endpoints

@app.post("/cocart-products", status_code=status.HTTP_201_CREATED)
def add_product_to_cocart(
    cocart_product_create: CocartProductCreate,
    db: Session = Depends(get_db)
):
    try:
        print("cocart_product_create", cocart_product_create)
        cocart = db.query(Cocart).filter(
            Cocart.id == cocart_product_create.cocart_id).first()
        if not cocart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cocart not found"
            )
        
        new_product = Product(
            name=cocart_product_create.product.name,
            original_price=cocart_product_create.product.original_price,
            price=cocart_product_create.product.price,
            slug=cocart_product_create.product.slug,
            added_by=cocart_product_create.product.added_by,
            customer_rating=cocart_product_create.product.customer_rating,
            product_tracking_url=cocart_product_create.product.product_tracking_url
        )

        if not new_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        new_product_image = ProductImage(
            product_id=new_product.id,
            image=cocart_product_create.product.image
        )
        db.add(new_product_image)
        db.commit()

        new_cocart_product = CocartProduct(
            cocart_id=cocart_product_create.cocart_id,
            product_id=new_product.id,
            note=cocart_product_create.note
        )
        db.add(new_cocart_product)
        db.commit()
        db.refresh(new_cocart_product)
        return {
            "message": "Product added to cocart successfully",
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/cocarts/{cocart_id}/products")
def get_cocart_products(cocart_id: int, db: Session = Depends(get_db)):
    try:
        cocart = db.query(Cocart).filter(
            Cocart.id == cocart_id).first()
        if not cocart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cocart not found"
            )

        products = (
            db.query(Product)
            .options(joinedload(Product.product_images))
            .join(CocartProduct, CocartProduct.product_id == Product.id)
            .filter(CocartProduct.cocart_id == cocart_id)
            .all()
        )

        response = []
        for product, note in products:
            response.append({
                "id": product.id,
                "name": product.name,
                "original_price": product.original_price,
                "customer_rating": product.customer_rating,
                "price": product.price,
                "product_tracking_url": product.product_tracking_url,
                "slug": product.slug,
                "added_by": product.added_by,
                "images": [
                    {
                        "image": image.image,
                        "thumbnail": image.thumbnail,
                        "medium_image": image.medium_image,
                        "large_image": image.large_image
                    }
                    for image in product.product_images
                ],
                "note": note  # Include the note here
            })

        return response
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Delete all data (admin operation)

@app.delete("/all_data")
def delete_all_data(password: str, db: Session = Depends(get_db)):
    if password != "adminadmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    try:
        db.query(CocartProduct).delete()
        db.query(Product).delete()
        db.query(Cocart).delete()
        db.query(User).delete()
        db.commit()
        return {"message": "All data deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
