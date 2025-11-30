from datetime import datetime
from pydantic import BaseModel

class Payments(BaseModel):
    payment_id: int
    order_id: int #FK
    amount: float
    payment_date: datetime
    method: str