ColumnNames = ['id', 'product_category_id', 'name', 'short_description', 'description', 'brand_name', 'product_tracking_url', 'standard_shipping_rate', 'size', 'color', 'marketplace', 'model_number', 'seller_info', 'customer_rating', 'number_of_reviews', 'rhid', 'bundle', 'clearance', 'preorder',
               'stock', 'freight', 'gender', 'affiliate_add_to_cart_url', 'max_number_of_qty', 'offer_type', 'available_online', 'e_delivery', 'deleted_at', 'created_at', 'updated_at', 'product_image_id', 'price', 'original_price', 'slug', 'wm_product_id', 'product_source', 'amazon_id', 'added_by']

product_images = ['id', 'product_id', 'image', 'thumbnail',
                  'medium_image', 'large_image', 'deleted_at', 'created_at', 'updated_at']


class ProductBase(BaseModel):
    title: str
    current_price: str
    mrp_price: str
    rating: str
    image_url: str
    url: str
    website_name: str
    note: str


# list matching columns in ProductBase and ColumnNames
product_cols = [
    'name', 'price', 'original_price', 'customer_rating', 'product_image_id', 'affiliate_add_to_cart_url', 'product_source']

# inside product_images
product_url = [
    'image', 'thumbnail', 'medium_image', 'large_image'
]
