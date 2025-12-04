from pydantic import BaseModel

class Orderitems(BaseModel):
    order_item_id: int
    order_id: int #FK
    product_id: int #FK
    quantity: int
    price: float | None