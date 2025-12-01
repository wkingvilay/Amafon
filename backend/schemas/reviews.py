from datetime import datetime
from pydantic import BaseModel, Field

class Reviews(BaseModel):
    product_id: int #FK
    user_id: int #FK
    rating: int = Field(..., ge=1, le=5)
    comment: str | None
    review_date: datetime

class ReviewsRead(Reviews):
    review_id: int