import json
from fastapi import FastAPI, Request, HTTPException, Depends, status, Body
from fastapi.middleware.cors import CORSMiddleware
from DB.database import Wishlist, Product, WishlistProduct
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


@app.get("/healthcheck")
def healthcheck(request: Request):
    return {
        "message": " Server is up and running",
        "domain": request.url.hostname,
    }


@app.get("/get_users")
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(Wishlist).distinct(Wishlist.user_id).all()
        return users
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


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


@app.delete("/delete_product/{product_id}")
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
def delete_all_data(password: str, db: Session = Depends(get_db)):
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


@app.get("/monitor-product")
async def scrape(db: Session = Depends(get_db)):
    key = os.getenv("SCRAPER_API")
    url = f"https://api.scraperapi.com?api_key={key}&url="

    products = db.query(Product).all()
    for product in products:
        product_url = product.url
        product_id = product.id
        response = requests.get(url + product_url)
        data = await scrape_product_data(response.text, product_url)
        product = UpdateProductBase(**data)
        update_product(product_id, product, db)
        print("Product data updated successfully for product_id: ", product_id)

    return {"message": "Product data updated successfully"}

# User Management Endpoints


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(Wishlist.user_id).distinct().all()
        user_ids = [user[0] for user in users]
        result = []
        for user_id in user_ids:
            wishlists = db.query(Wishlist).filter_by(user_id=user_id).all()
            result.append({"user_id": user_id, "wishlists": wishlists})
        return result
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/users/{user_id}")
def get_user_wishlists(user_id: str, db: Session = Depends(get_db)):
    try:
        wishlists = db.query(Wishlist).filter_by(user_id=user_id).all()
        if not wishlists:
            return {"message": "User not found or no wishlists"}
        return {"user_id": user_id, "wishlists": wishlists}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

# Wishlist Monitoring Endpoints


@app.get("/wishlists")
def get_all_wishlists(db: Session = Depends(get_db), user_id: str = None):
    try:
        if user_id:
            wishlists = db.query(Wishlist).filter_by(user_id=user_id).all()
        else:
            wishlists = db.query(Wishlist).all()
        return wishlists
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/wishlists/filter")
def filter_wishlists(user_id: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Wishlist)
        if user_id:
            query = query.filter(Wishlist.user_id == user_id)
        if start_date:
            query = query.filter(Wishlist.created_at >= start_date)
        if end_date:
            query = query.filter(Wishlist.created_at <= end_date)
        wishlists = query.all()
        return wishlists
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

# System Analytics Dashboard Endpoints


@app.get("/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    try:
        total_users = db.query(Wishlist.user_id).distinct().count()
        total_wishlists = db.query(Wishlist).count()
        total_products = db.query(Product).count()

        # Top products added
        top_products = db.query(Product.title, func.count(WishlistProduct.product_id).label('count'))\
            .join(WishlistProduct).group_by(Product.id).order_by(func.count(WishlistProduct.product_id).desc()).limit(5).all()

        top_products_list = [{"title": product[0],
                              "count": product[1]} for product in top_products]

        return {
            "total_users": total_users,
            "total_wishlists": total_wishlists,
            "total_products": total_products,
            "top_products": top_products_list
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/analytics/user-engagement")
def get_user_engagement(db: Session = Depends(get_db)):
    """
    Get average number of wishlists per user and average number of products per wishlist
    """

    try:
        total_users = db.query(Wishlist.user_id).distinct().count()
        total_wishlists = db.query(Wishlist).count()
        avg_wishlists_per_user = total_wishlists / total_users if total_users else 0

        total_wishlist_products = db.query(WishlistProduct).count()
        avg_products_per_wishlist = total_wishlist_products / \
            total_wishlists if total_wishlists else 0

        return {
            "avg_wishlists_per_user": avg_wishlists_per_user,
            "avg_products_per_wishlist": avg_products_per_wishlist
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


@app.get("/analytics/product-trends")
def get_product_trends(db: Session = Depends(get_db)):
    """
    Get number of products added over time
    """
    try:
        products_over_time = db.query(func.date(WishlistProduct.added_at), func.count(WishlistProduct.id))\
            .group_by(func.date(WishlistProduct.added_at)).order_by(func.date(WishlistProduct.added_at)).all()

        trends = [{"date": str(item[0]), "count": item[1]}
                  for item in products_over_time]

        return trends
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

# Report Generation Endpoint


@app.get("/reports/{report_type}")
def generate_report(report_type: str, db: Session = Depends(get_db)):
    try:
        if report_type == "user_activity":
            users = db.query(Wishlist.user_id, Wishlist.created_at).all()
            data = [{"user_id": user[0], "created_at": str(
                user[1])} for user in users]
            df = pd.DataFrame(data)
        else:
            return {"error": "Invalid report type"}

        # Generate Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                "Content-Disposition": f"attachment; filename={report_type}.xlsx"
            }
        )
    except Exception as e:
        return {"error": str(e)}
