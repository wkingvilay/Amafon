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

@router.get("/all/list")
async def api_get_all_orders():
    """Get all orders with their items for display"""
    async with database:
        # Get all orders
        orders_query = "SELECT * FROM Orders ORDER BY order_date DESC"
        orders = await database.fetch_all(orders_query)
        
        result = []
        for order in orders:
            order_dict = dict(order)
            
            # Get order items for this order
            items_query = """
                SELECT oi.quantity, p.name, p.price, oi.price as order_price
                FROM OrderItems oi
                JOIN Products p ON oi.product_id = p.product_id
                WHERE oi.order_id = :order_id
            """
            items = await database.fetch_all(items_query, {"order_id": order_dict["order_id"]})
            
            # Format items as string
            if items:
                items_list = []
                for item in items:
                    items_list.append(f"{item['quantity']}x {item['name']} - ${float(item['order_price']) * item['quantity']:.2f}")
                order_dict['items'] = "; ".join(items_list)
            else:
                order_dict['items'] = "No items"
            
            result.append(order_dict)
        
        return result

@router.put("/{order_id}/status")
async def api_update_order_status(order_id: int, status_data: dict):
    """Update order status"""
    async with database:
        new_status = status_data.get("status")
        if not new_status:
            raise HTTPException(status_code=400, detail="Status is required")
        
        query = "UPDATE Orders SET status = :status WHERE order_id = :order_id"
        await database.execute(query, {"status": new_status, "order_id": order_id})
        
        # Fetch updated order
        row = await database.fetch_one("SELECT * FROM Orders WHERE order_id = :id", {"id": order_id})
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        return dict(row)

@router.delete("/delete/{order_id}")
async def api_delete_order_alt(order_id: int):
    """Alternative delete endpoint"""
    async with database:
        deleted = await delete_order(order_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"detail": "Order deleted", "success": True}

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
            
            print(f"Creating order for user {user_id}, address: {shipping_address}")
            order_id = await create_order(user_id, "Pending", shipping_address)
            print(f"Order created with ID: {order_id}")
            
            # Add order items
            items = order_data.get("items", [])
            print(f"Processing {len(items)} items: {items}")
            
            for item in items:
                product_id = item.get("product_id")
                quantity = item.get("quantity", 1)
                
                if product_id:
                    print(f"Adding item: product_id={product_id}, quantity={quantity}")
                    await create_orderitem(order_id, product_id, quantity)
                else:
                    print(f"Skipping item without product_id: {item}")
            
            # Fetch and return the created order
            row = await database.fetch_one(
                "SELECT * FROM Orders WHERE order_id = :id", 
                {"id": order_id}
            )
            
            print(f"Order complete. Final order: {dict(row) if row else None}")
            return {"success": True, "order_id": order_id, "order": dict(row) if row else None}
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-demo")
async def create_demo_order():
    from ..crud.orders_crud import create_order
    
    async with database:
        # Hard-coded order
        user_id = 1
        status = "Pending"
        shipping_address = "123 Demo St"
        
        order_id = await create_order(user_id, status, shipping_address)
        
        row = await database.fetch_one("SELECT * FROM Orders WHERE order_id = :id", {"id": order_id})
        
        return row  # will return dict representing the DB row