from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)  # Optional name for the wishlist
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship with wishlist_products table
    wishlist_items = relationship(
        "WishlistProduct",
        back_populates="wishlist",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Relationship to products through wishlist_products
    products = relationship(
        "Product",
        secondary="wishlist_products",
        back_populates="wishlists",
        cascade="all, delete",
        passive_deletes=True,
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(
        String(255), nullable=False, index=True
    )  
    current_price = Column(String(255), nullable=False)
    mrp_price = Column(String(255), nullable=False)
    rating = Column(String(50), nullable=False)
    image_url = Column(
        String(500), nullable=True, server_default=None
    )  # Increased to 500 chars
    url = Column(Text, nullable=False)  # Use Text for long URLs
    website_name = Column(
        String(100), nullable=False
    )  # Limiting website name to 100 chars
    note = Column(Text, nullable=True)  # Use Text for long notes

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    wishlist_items = relationship(
        "WishlistProduct",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Relationship to wishlists through wishlist_products
    wishlists = relationship(
        "Wishlist",
        secondary="wishlist_products",
        back_populates="products",
        passive_deletes=True,
    )


class WishlistProduct(Base):
    __tablename__ = "wishlist_products"

    id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(
        Integer,
        ForeignKey("wishlist.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    added_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships to Wishlist and Product tables
    wishlist = relationship("Wishlist", back_populates="wishlist_items")
    product = relationship("Product", back_populates="wishlist_items")
