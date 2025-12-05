from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Method(str, Enum):
    credit_card = "Credit Card"
    paypal = "PayPal"
    gift_card = "Gift Card"

class Payments(BaseModel):
    payment_id: int
    order_id: int | None #FK
    amount: float
    payment_date: datetime
    method: Method = Method.credit_card
    card_last4: str
    billing_address: str