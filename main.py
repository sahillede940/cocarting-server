from fastapi import FastAPI, Request, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List

from DB.models import User, Wishlist, Product, WishlistProduct, ProductImage
from DB.schemas import (
    UserCreate, User as UserSchema,
    WishlistCreate, Wishlist as WishlistSchema,
    WishlistProductCreate, UpdateProductBase
)
from DB.database import engine, get_db, Base
from sqlalchemy.orm import joinedload
import requests
import os
from BackgroundMonitoring import scrape_product_data
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler


Base.metadata.create_all(bind=engine)
app = FastAPI()

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
        # Update the Product fields
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

        # Update the ProductImage fields, if image is provided
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

# Wishlist Endpoints


@app.post("/wishlists", response_model=WishlistSchema, status_code=status.HTTP_201_CREATED)
def create_wishlist(wishlist_create: WishlistCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(
            User.id == wishlist_create.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        new_wishlist = Wishlist(
            name=wishlist_create.name,
            user_id=wishlist_create.user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_wishlist)
        db.commit()
        db.refresh(new_wishlist)
        return new_wishlist
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/wishlists/{user_id}", response_model=List[WishlistSchema])
def get_wishlists(user_id: int, db: Session = Depends(get_db)):
    try:
        wishlists = db.query(Wishlist).filter(
            Wishlist.user_id == user_id).all()
        return wishlists
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.delete("/wishlists/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
    try:
        # delete all products in the wishlist
        db.query(WishlistProduct).filter(
            WishlistProduct.wishlist_id == wishlist_id).delete()
        db.commit()

        wishlist = db.query(Wishlist).filter(
            Wishlist.id == wishlist_id).first()
        if not wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )
        db.delete(wishlist)
        db.commit()

        return {"message": "Wishlist deleted successfully"}

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

        wishlist_product = db.query(WishlistProduct).filter(
            WishlistProduct.product_id == product_id).first()
        if wishlist_product:
            db.delete(wishlist_product)
            db.commit()

        return {"message": "Product deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# WishlistProduct Endpoints


@app.post("/wishlist-products", status_code=status.HTTP_201_CREATED)
def add_product_to_wishlist(
    wishlist_product_create: WishlistProductCreate,
    db: Session = Depends(get_db)
):
    try:
        # Check if wishlist exists
        wishlist = db.query(Wishlist).filter(
            Wishlist.id == wishlist_product_create.wishlist_id).first()
        if not wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )
        # Check if product exists
        new_product = Product(
            name=wishlist_product_create.product.name,
            original_price=wishlist_product_create.product.original_price,
            price=wishlist_product_create.product.price,
            slug=wishlist_product_create.product.slug,
            added_by=wishlist_product_create.product.added_by,
            customer_rating=wishlist_product_create.product.customer_rating,
            product_tracking_url=wishlist_product_create.product.product_tracking_url
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
            image=wishlist_product_create.product.image
        )
        db.add(new_product_image)
        db.commit()

        new_wishlist_product = WishlistProduct(
            wishlist_id=wishlist_product_create.wishlist_id,
            product_id=new_product.id,
            note=wishlist_product_create.note
        )
        db.add(new_wishlist_product)
        db.commit()
        db.refresh(new_wishlist_product)
        return {
            "message": "Product added to wishlist successfully",
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/wishlists/{wishlist_id}/products")
def get_wishlist_products(wishlist_id: int, db: Session = Depends(get_db)):
    try:
        wishlist = db.query(Wishlist).filter(
            Wishlist.id == wishlist_id).first()
        if not wishlist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist not found"
            )

        # Query products with related ProductImage objects
        products = (
            db.query(Product)
            .options(joinedload(Product.product_images))  # Load related images
            .join(WishlistProduct, WishlistProduct.product_id == Product.id)
            .filter(WishlistProduct.wishlist_id == wishlist_id)
            .all()
        )

        # Format the response to include images within each product
        response = []
        for product in products:
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
                ]
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
        db.query(WishlistProduct).delete()
        db.query(Product).delete()
        db.query(Wishlist).delete()
        db.query(User).delete()
        db.commit()
        return {"message": "All data deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
