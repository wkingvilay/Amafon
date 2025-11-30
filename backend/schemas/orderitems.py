from pydantic import BaseModel

class Orderitems(BaseModel):
    order_id: int #FK
    product_id: int #FK
    quantity: int
    price: float | None

class OrderitemsRead(Orderitems):
    orderitem_id: int