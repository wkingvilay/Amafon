from database import database
from fastapi import APIRouter, HTTPException
from schemas.orders import Orders
from crud.orders_crud import get_user_orders, get_order, create_order, update_order, delete_order

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/orders/{user_id}", response_model=list[Orders])
async def api_get_user_orders(user_id: int):
    async with database:
        rows = await get_user_orders(user_id)
        return [Orders(**dict(r)) for r in rows]

@router.get("/{order_id}", response_model=Orders)
async def api_get_order(order_id: int):
    async with database:
        d = await get_order(order_id)
        if not d:
            raise HTTPException(status_code=404, detail="Order not found")
        return Orders(**dict(d))

@router.post("/", response_model=Orders)
async def api_create_order(order: Orders):
    async with database:
        try:
            order_id = await create_order(order.user_id, order.status, order.shipping_address)
            row = await database.fetch_one(
                "SELECT * FROM Orders WHERE order_id = :id",
                {"id": order_id}
            )
            return Orders(**row)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=Orders)
async def api_update_order(order: Orders):
    async with database:
        try:
            await update_order(order.status, order.shipping_address, order.order_id)
            return Orders(**order.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{order_id}")
async def api_delete_order(order_id: int):
    async with database:
        deleted = await delete_order(order_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"detail": "Order deleted"}