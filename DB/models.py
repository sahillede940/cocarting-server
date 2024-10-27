from sqlalchemy import Column, ForeignKey, Integer, String, Text, Double, TIMESTAMP, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from DB.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)

    wishlists = relationship("Wishlist", back_populates="user")


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
    product_id = Column(BigInteger, ForeignKey("products.id"), nullable=True)
    image = Column(Text, nullable=True)
    thumbnail = Column(String(255), nullable=True)
    medium_image = Column(String(255), nullable=True)
    large_image = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    product = relationship("Product", back_populates="product_images")


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    user = relationship("User", back_populates="wishlists")
    products = relationship("WishlistProduct", back_populates="wishlist")


class WishlistProduct(Base):
    __tablename__ = "wishlist_products"

    id = Column(BigInteger, primary_key=True, index=True)
    wishlist_id = Column(BigInteger, ForeignKey("wishlists.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    note = Column(Text, nullable=True)

    wishlist = relationship("Wishlist", back_populates="products")
    product = relationship("Product")

