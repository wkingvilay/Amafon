from database import database
from schemas.orders import Status

# Returns the information for orders from a specific user
async def get_user_orders(user_id: int):
    query="""
    SELECT * FROM Orders
    WHERE user_id = :user_id
    """
    return await database.fetch_all(query=query, values={"user_id": user_id})

# Returns the information in an order based on order_id
async def get_order(order_id: int):
    query="""
    SELECT * FROM Orders
    WHERE order_id = :order_id;
    """
    row = await database.fetch_one(query=query, values={"order_id": order_id})
    return dict(row) if row else None

# Create an order
async def create_order(user_id: int, status: Status, shipping_address: str):
    query="""
    INSERT INTO Orders (user_id, status,  total_amount, shipping_address)
    VALUES (:user_id, :status, 0, :shipping_address);
    """
    try:
        await database.execute(query=query, values={"user_id": user_id, "status": status, "shipping_address": shipping_address})
        return await database.fetch_val("SELECT LAST_INSERT_ID();")
    except Exception:
        raise ValueError("Something went wrong with order creation")

# Update an order based on order_id (costs can be modified by changing orderitem entries)
async def update_order(status: Status, shipping_address: str, order_id: int):
    query="""
    UPDATE Orders SET status = :status, shipping_address = :shipping_address 
    WHERE order_id = :order_id;
    """
    try:
        await database.execute(query=query, values={"status": status, "shipping_address": shipping_address, "order_id": order_id})
        return True
    except Exception:
        raise ValueError("Something went wrong with order update")

# Delete an order based on order_id
async def delete_order(order_id: int):
    query="DELETE FROM Orders WHERE order_id = :order_id"
    try:
        await database.execute(query=query, values={"order_id": order_id})
        return True
    except:
        return False