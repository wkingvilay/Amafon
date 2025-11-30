from pydantic import BaseModel

class Sellers(BaseModel):
    user_id: int #FK
    brand_name: str | None

class SellersRead(Sellers):
    seller_id: int