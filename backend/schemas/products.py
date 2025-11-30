from pydantic import BaseModel

class Products(BaseModel):
    seller_id: int #FK
    category_id: int #FK
    name: str | None
    description: str | None
    price: float | None # Might need validation,
    stock: int

class ProductsRead(Products):
    product_id: int