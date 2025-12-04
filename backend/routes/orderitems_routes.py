from ..database import database
from fastapi import APIRouter, HTTPException
from ..schemas.orderitems import Orderitems
from ..crud.orderitems_crud import get_orderitems, create_orderitem, update_orderitem, delete_orderitem

router = APIRouter(prefix="/api/orderitems", tags=["Orderitems"])

@router.get("/", response_model=list[Orderitems])
async def api_get_orderitems(order_id: int):
    async with database:
        rows = await get_orderitems(order_id)
        return [Orderitems(**dict(r)) for r in rows]

@router.post("/", response_model=Orderitems)
async def api_create_orderitem(orderitem: Orderitems):
    async with database:
        try:
            order_item_id = await create_orderitem(orderitem.order_id, orderitem.product_id, orderitem.quantity)
            row = await database.fetch_one(
                "SELECT * FROM orderitems WHERE order_item_id = :id",
                {"id": order_item_id}
            )
            return Orderitems(**row)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=Orderitems)
async def api_update_orderitem(orderitem: Orderitems):
    async with database:
        try:
            await update_orderitem(orderitem.quantity, orderitem.orderitem_id)
            return Orderitems(**orderitem.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{orderitem_id}")
async def api_delete_orderitem(orderitem_id: int):
    async with database:
        deleted = await delete_orderitem(orderitem_id)
        if not deleted:
            raise HTTPException(404, "Order item not found")
        return {"detail": "Order item deleted"}