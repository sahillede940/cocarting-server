from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    original_price: float
    customer_rating: str
    price: float
    product_source: int
    image: str


class WishlistBase(BaseModel):
    id: int
    
class CreateWishlistBase(BaseModel):
    id: int
    name: str


class AddToWishlist(BaseModel):
    product: ProductBase
    wishlist: WishlistBase
