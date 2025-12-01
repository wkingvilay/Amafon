from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Method(str, Enum):
    credit_card = "credit_card"
    paypal = "paypal"
    gift_card = "gift_card"

class Payments(BaseModel):
    order_id: int | None #FK
    amount: float
    payment_date: datetime
    method: Method = Method.credit_card

class PaymentsRead(Payments):
    payment_id: int