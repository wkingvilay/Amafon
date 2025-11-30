from database import database
from fastapi import APIRouter, HTTPException
from schemas.orderitems import Orderitems, OrderitemsRead
from crud.orderitems_crud import get_orderitems, create_orderitem, update_orderitem, delete_orderitem

router = APIRouter(prefix="/api/orderitems", tags=["Orderitems"])

@router.get("/", response_model=list[OrderitemsRead])
async def api_get_orderitems(order_id: int):
    async with database:
        rows = await get_orderitems(order_id)
        return [OrderitemsRead(**dict(r)) for r in rows]

@router.post("/", response_model=OrderitemsRead)
async def api_create_orderitem(orderitem: Orderitems):
    async with database:
        try:
            orderitem_id = await create_orderitem(orderitem.order_id, orderitem.product_id, orderitem.quantity)
            return OrderitemsRead(orderitem_id=orderitem_id, **orderitem.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=OrderitemsRead)
async def api_update_orderitem(orderitem: OrderitemsRead):
    async with database:
        try:
            await update_orderitem(orderitem.quantity, orderitem.orderitem_id)
            return OrderitemsRead(**orderitem.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{orderitem_id}")
async def api_delete_orderitem(orderitem_id: int):
    async with database:
        deleted = await delete_orderitem(orderitem_id)
        if not deleted:
            raise HTTPException(404, "Order item not found")
        return {"detail": "Order item deleted"}