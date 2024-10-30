from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

# URL encode the password

load_dotenv()


DB_CONNECTION = os.getenv("DB_CONNECTION")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
encoded_password = urllib.parse.quote(DB_PASSWORD)


# mysql connection string
DATABASE_URL = f"{DB_CONNECTION}://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
print(Base.classes.keys())  # This will show all table names SQLAlchemy recognizes


# User = Base.classes.get("users")  # Using .get() will prevent KeyError if the table is not found
# Product = Base.classes.get("products")
# ProductImage = Base.classes.get("product_images")
# Cocart = Base.classes.get("cocarts")
# CocartProduct = Base.classes.get("cocart_products")

