from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Status(str, Enum):
    pending = "pending"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "cancelled"

class Orders(BaseModel):
    user_id: int #FK
    order_date: datetime
    total_amount: float | None
    status: Status = Status.pending

class OrdersRead(Orders):
    order_id: int