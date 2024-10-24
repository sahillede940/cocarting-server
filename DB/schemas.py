from pydantic import BaseModel


class WishlistBase(BaseModel):
    user_id: str
    name: str


class ProductBase(BaseModel):
    title: str
    current_price: str
    mrp_price: str
    rating: str
    image_url: str
    url: str
    website_name: str
    note: str

class UpdateProductBase(BaseModel):
    title: str
    current_price: str
    mrp_price: str
    rating: str
    image_url: str
    url: str
    website_name: str


class WishlistProductBase(BaseModel):
    wishlist_id: int
    product_id: int
