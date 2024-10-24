import json
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from DB.models import Wishlist, Product, WishlistProduct
from DB.schemas import ProductBase, WishlistBase, UpdateProductBase
from DB.database import engine, get_db, Base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Body
import requests
from dotenv import load_dotenv
import os
from BackgroundMonitoring import scrape_product_data

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


@app.post("/create_wishlist")
def create_wishlist(wishlist: WishlistBase, db: Session = Depends(get_db)):
    try:
        new_wishlist = Wishlist(name=wishlist.name, user_id=wishlist.user_id)
        db.add(new_wishlist)
        db.commit()
        db.refresh(new_wishlist)
        return new_wishlist
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

# delete wishlist
@app.delete("/delete_wishlist/{wishlist_id}")
def delete_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
    try:
        wishlist = db.query(Wishlist).filter_by(id=wishlist_id).first()
        db.delete(wishlist)
        db.commit()
        return {"message": "Wishlist deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

@app.get("/get_wishlists/{user_id}")
def get_wishlist(user_id: str, db: Session = Depends(get_db)):
    try:
        wishlists = db.query(Wishlist).filter_by(user_id=user_id).all()
        return wishlists
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.post("/add_to_wishlist")
def add_to_wishlist(
    product: ProductBase, wishlist_id: int = Body(...), db: Session = Depends(get_db)
):
    try:
        new_product = Product(**product.model_dump())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        wishlist_product = WishlistProduct(
            wishlist_id=wishlist_id, product_id=new_product.id
        )
        db.add(wishlist_product)
        db.commit()
        db.refresh(wishlist_product)
        return wishlist_product
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_wishlist_products/{wishlist_id}")
def get_wishlist_products(wishlist_id: int, db: Session = Depends(get_db)):
    try:
        products = (
            db.query(Product)
            .join(WishlistProduct)
            .join(Wishlist)
            .filter(WishlistProduct.wishlist_id == wishlist_id)
            .order_by(Product.created_at.desc())
            .all()
        )
        return products
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}
    
@app.delete("/delete_product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter_by(id=product_id).first()
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}



@app.delete("/all_data")
def delete_all_data(password:str, db: Session = Depends(get_db)):
    print("ALL DATA DELETED")
    if password != "adminadmin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password", 
        )
    try:
        db.query(WishlistProduct).delete()
        db.query(Product).delete()
        db.query(Wishlist).delete()
        db.commit()
        return {"message": "All data deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}
    

def update_product(product_id: int, product: UpdateProductBase, db: Session):
    try:
        db.query(Product).filter_by(id=product_id).update(product.model_dump())
        db.commit()
        return {"message": "Product updated successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/scrape")
async def scrape(product_url: str, product_id:int, db: Session = Depends(get_db)):
    key = os.getenv("SCRAPER_API")    
    url = f"https://api.scraperapi.com?api_key={key}&url=" + product_url
    response = requests.get(url)
    data = await scrape_product_data(response.text, product_url)
    product = UpdateProductBase(**data)
    return update_product(product_id, product, db)
