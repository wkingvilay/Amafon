from pydantic import BaseModel
from datetime import datetime

class Sellers(BaseModel):
    seller_id: int
    user_id: int #FK
    store_name: str | None
    rating: float = 0.0
    created_at: datetime