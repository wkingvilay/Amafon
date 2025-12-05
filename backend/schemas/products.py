from pydantic import BaseModel
from datetime import datetime

class Products(BaseModel):
    product_id: int
    seller_id: int #FK
    category_id: int #FK
    name: str | None
    description: str | None
    price: float | None 
    stock: int
    image_url: str | None
    is_active: bool = True
    created_at: datetime 
    updated_at: datetime