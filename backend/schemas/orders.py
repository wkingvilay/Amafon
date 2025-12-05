from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    Pending = "Pending"
    Paid = "Paid"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Canceled = "Cancelled"

class Orders(BaseModel):
    order_id: int
    user_id: int #FK
    order_date: datetime
    total_amount: float = 0
    status: Status = Status.Pending
    shipping_address: str | None