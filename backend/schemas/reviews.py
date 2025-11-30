from datetime import datetime
from pydantic import BaseModel

class Reviews(BaseModel):
    review_id: int
    product_id: int #FK
    user_id: int #FK
    rating: int
    comment: str | None
    review_date: datetime