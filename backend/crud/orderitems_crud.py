from ..database import database

# Gets order items from an order based on order_id
async def get_orderitems(order_id: int):
    query="""
    SELECT * From Orderitems JOIN Orders ON Orders.order_id = Orderitems.order_id
    WHERE Orders.order_id = :order_id
    """
    return await database.fetch_all(query=query, values={"order_id": order_id})

# Creates a new order item; updates order price automatically
async def create_orderitem(order_id: int, product_id: int, quantity: int):
    price_query = "SELECT price FROM Products WHERE product_id = :product_id"
    product = await database.fetch_one(price_query, values={"product_id": product_id})
    if not product:
        raise ValueError("Product not found")
    price = product["price"]

    query = """
    INSERT INTO orderitems (order_id, product_id, quantity, price)
    VALUES (:order_id, :product_id, :quantity, :price)
    """
    try:
        await database.execute(query=query, values={
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        })
    except Exception:
        raise ValueError("Something went wrong with order item creation")
    # update the order's total
    try:
        await update_order_total(order_id=order_id)
    except Exception:
        raise ValueError("Something went wrong with order item update")
    
    return await database.fetch_val("SELECT LAST_INSERT_ID();")

# Updates the quantity of items in an entry (I keep saying this, but FK are usually immutable)
async def update_orderitem(quantity: int, order_item_id: int):
    price_query = """
        SELECT p.price FROM products p JOIN orderitems oi
        ON oi.product_id = p.product_id WHERE oi.order_item_id = :order_item_id
    """
    product = await database.fetch_one(price_query, values={"order_item_id": order_item_id})
    if not product:
        raise ValueError("Product not found")
    price = product["price"]

    query="""
    UPDATE orderitems SET quantity = :quantity, price = :price
    WHERE order_item_id = :order_item_id      
    """
    try:
        await database.execute(query=query, values={"quantity": quantity, "price": price, "order_item_id": order_item_id})
    except Exception:
        raise ValueError("Error updating order item")
    try:
        order_id_query="""
            SELECT order_id FROM orderitems 
            WHERE order_item_id = :order_item_id 
        """
        row = await database.fetch_one(query=order_id_query, values={"order_item_id": order_item_id})
        if not row:
            raise ValueError("Order item not found")
        order_id = row["order_id"]
        await update_order_total(order_id=order_id)
    except Exception:
        raise ValueError("Something went wrong with order item update")

# Deletes an orderitem entry based on order_item_id
async def delete_orderitem(order_item_id: int):
    # Get the order_id before deletion
    order_id_query = """ \
                     SELECT order_id \
                     FROM orderitems \
                     WHERE order_item_id = :order_item_id \
                   """
    row = await database.fetch_one(query=order_id_query, values={"order_item_id": order_item_id})
    if not row:
        raise ValueError("Order item not found")

    order_id = row["order_id"]
    query="DELETE FROM orderitems WHERE order_item_id = :order_item_id"
    try:
        await database.execute(query=query, values={"order_item_id": order_item_id})
    except:
        return False
    try:
        await update_order_total(order_id=order_id)
    except Exception:
        raise ValueError("Something went wrong with order item update")
    return True

# Helper function to update orders when orderitems are created, updated, or deleted
async def update_order_total(order_id: int):
    query="""
    UPDATE orders
    SET total_amount = (
        SELECT sum(p.price * oi.quantity) AS total 
        FROM orderitems oi JOIN products p ON oi.product_id = p.product_id 
        WHERE oi.order_id = :order_id
    ) 
    WHERE order_id = :order_id
    """
    await database.execute(query=query, values={"order_id": order_id})
    return
