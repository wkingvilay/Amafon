from ..database import database
from fastapi import APIRouter, HTTPException
from ..schemas.orders import Orders
from datetime import datetime
from ..crud.orders_crud import get_user_orders, get_order, create_order, update_order, delete_order

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

@router.post("/create-from-cart")
async def create_order_from_cart(order_data: dict):
    """
    Create an order from cart data
    Expected format:
    {
        "user_id": 1,
        "shipping_address": "123 Main St",
        "items": [{"product_id": 1, "name": "Product", "price": 10.99, "quantity": 1}],
        "total": 15.99
    }
    """
    from ..crud.orders_crud import create_order
    from ..crud.orderitems_crud import create_orderitem
    
    async with database:
        try:
            # Create the order
            user_id = order_data.get("user_id", 1)
            shipping_address = order_data.get("shipping_address", "Not provided")
            total = order_data.get("total", 0)
            
            order_id = await create_order(user_id, "Pending", shipping_address)
            
            # Add order items
            items = order_data.get("items", [])
            for item in items:
                product_id = item.get("product_id")
                quantity = item.get("quantity", 1)
                
                if product_id:
                    await create_orderitem(order_id, product_id, quantity)
            
            # Fetch and return the created order
            row = await database.fetch_one(
                "SELECT * FROM Orders WHERE order_id = :id", 
                {"id": order_id}
            )
            
            return {"success": True, "order_id": order_id, "order": dict(row) if row else None}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
router = APIRouter(prefix="/api/orders")

@router.post("/create-demo")
async def create_demo_order():
    from ..crud.orders_crud import create_order
    
    # Hard-coded order
    user_id = 1
    status = "Pending"
    shipping_address = "123 Demo St"
    
    order_id = await create_order(user_id, status, shipping_address)
    
    row = await database.fetch_one("SELECT * FROM Orders WHERE order_id = :id", {"id": order_id})
    
    return row  # will return dict representing the DB row