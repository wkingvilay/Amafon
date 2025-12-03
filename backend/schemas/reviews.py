from datetime import datetime
from pydantic import BaseModel, Field

class Reviews(BaseModel):
    review_id: int
    product_id: int #FK
    user_id: int #FK
    rating: int = Field(..., ge=1, le=5)
    title: str | None
    comment: str | None
    review_date: datetime