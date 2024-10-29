from sqlalchemy import Column, ForeignKey, Integer, String, Text, Double, TIMESTAMP, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from DB.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)

    cocarts = relationship("Cocart", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    original_price = Column(Double, nullable=True)
    customer_rating = Column(String(255), nullable=True)
    price = Column(Double, nullable=True)
    product_tracking_url = Column(String(2500), nullable=True)
    slug = Column(String(255), unique=True, nullable=False)
    added_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)

    product_source = Column(Integer, default=0)
    short_description = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    brand_name = Column(String(255), nullable=True)
    standard_shipping_rate = Column(String(255), nullable=True)
    size = Column(String(255), nullable=True)
    color = Column(String(255), nullable=True)
    marketplace = Column(Integer, default=0)
    model_number = Column(String(255), nullable=True)
    seller_info = Column(String(255), nullable=True)
    number_of_reviews = Column(Integer, nullable=True)
    rhid = Column(String(255), nullable=True)
    bundle = Column(Boolean, default=True)
    clearance = Column(Boolean, default=True)
    preorder = Column(Boolean, default=True)
    stock = Column(String(255), nullable=True)
    freight = Column(Boolean, default=True)
    gender = Column(String(255), default='m')
    affiliate_add_to_cart_url = Column(String(2500), nullable=True)
    max_number_of_qty = Column(Integer, nullable=True)
    offer_type = Column(Integer, nullable=True)
    available_online = Column(Boolean, default=False)
    e_delivery = Column(Boolean, default=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    wm_product_id = Column(String(255), nullable=True)
    amazon_id = Column(String(255), nullable=True)

    product_images = relationship("ProductImage", back_populates="product")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(BigInteger, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False, index=True)
    image = Column(Text, nullable=True)
    thumbnail = Column(String(255), nullable=True)
    medium_image = Column(String(255), nullable=True)
    large_image = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    product = relationship("Product", back_populates="product_images")


class Cocart(Base):
    __tablename__ = "cocarts"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(255), unique=True, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True, default=None)
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    thumbnail = Column(String(255), nullable=True)
    allow_vote = Column(Boolean, nullable=False, default=False)
    allow_add_product = Column(Boolean, nullable=False, default=False)
    allow_remove_product = Column(Boolean, nullable=False, default=False)
    mark_purchased_items = Column(Boolean, nullable=False, default=False)
    is_read = Column(Boolean, nullable=False, default=False)
    is_hide = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="cocarts")
    products = relationship("CocartProduct", back_populates="cocart")



class CocartProduct(Base):
    __tablename__ = "cocart_products"

    id = Column(BigInteger, primary_key=True, index=True)
    cocart_id = Column(BigInteger, ForeignKey("cocarts.id", ondelete="CASCADE"), nullable=True, index=True)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    deleted_at = Column(TIMESTAMP, nullable=True, default=None)
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_bought = Column(Boolean, nullable=False, default=False)
    is_claimed = Column(Boolean, nullable=False, default=False)
    note = Column(Text, nullable=True) # Note for the product is not present

    cocart = relationship("Cocart", back_populates="products")
    product = relationship("Product")



