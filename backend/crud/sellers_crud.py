from ..database import database

# Returns all the information for a specific seller based on seller_id
async def get_seller(seller_id: int):
    query = """
    SELECT * FROM Sellers
    WHERE seller_id = :seller_id
    """
    row = await database.fetch_one(query=query, values={"seller_id": seller_id})
    return dict(row) if row else None

# Creates a new seller
async def create_seller(user_id: int, store_name: str, rating: float = 0.0):
    query = """
    INSERT INTO Sellers (user_id, store_name, rating)
    VALUES (:user_id, :store_name, :rating)
    """
    try:
        await database.execute(query=query, values={
            "user_id": user_id,
            "store_name": store_name,
            "rating": rating
        })
        return await database.fetch_val("SELECT LAST_INSERT_ID();")
    except Exception:
        # Raise clear error if code already exists (email already in use)
        raise ValueError(f"Something went wrong with seller creation.")

# Updates an existing seller based on seller_id (user_id is immutable)
async def update_seller(store_name: str, seller_id: int, rating: float = 0.0):
    query = """
    UPDATE Sellers SET store_name = :store_name, rating = :rating
    WHERE seller_id = :seller_id
    """
    try:
        await database.execute(query=query, values={
            "store_name": store_name,
            "seller_id": seller_id,
            "rating": rating
        })
        return True
    except Exception:
        raise ValueError(f"Error updating seller")

# Deletes a seller based on seller_id
async def delete_seller(seller_id: int):
    query = "DELETE FROM Sellers WHERE seller_id = :seller_id"
    try:
        await database.execute(query=query, values={"seller_id": seller_id})
        return True
    except:
        return False