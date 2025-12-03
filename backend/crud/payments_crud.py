from database import database
from schemas.payments import Method

# Returns payment info based on payment_id
async def get_payment(payment_id: int):
    query = "SELECT * FROM payments WHERE payment_id = :payment_id"
    row = await database.fetch_one(query=query, values={"payment_id": payment_id})
    return dict(row) if row else None

# Returns any payments related to an order based on order_id
async def get_payments_by_order(order_id: int):
    query = "SELECT * FROM payments WHERE order_id = :order_id"
    return await database.fetch_all(query, {"order_id": order_id})

# Creates a new payment entry
async def create_payment(order_id: int, amount: float, method: Method, card_last4: str, billing_address: str):
    query = """
    INSERT INTO Payments(order_id, amount, method, card_last4, billing_address)
    VALUES (:order_id, :amount, :method, :card_last4, :billing_address)
    """
    try:
        await database.execute(query=query, values={
            "order_id": order_id,
            "amount": amount,
            "method": method,
            "card_last4": card_last4,
            "billing_address": billing_address
        })
        return await database.fetch_val("SELECT LAST_INSERT_ID();")
    except Exception:
        raise ValueError(f"Something went wrong with payment creation.")

# No update method; doesn't make sense to allow payment records to change

# Deletes a payment based on payment_id (for administrative purposes)
async def delete_payment(payment_id: int):
    query = "DELETE FROM Payments WHERE payment_id = :payment_id"
    try:
        await database.execute(query=query, values={"payment_id": payment_id})
        return True
    except:
        return False

