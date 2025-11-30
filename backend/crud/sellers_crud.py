from database import database

# Returns all the information for a specific seller based on seller_id
async def get_seller(seller_id: int):
    query = """
    SELECT * FROM Sellers
    WHERE seller_id = :seller_id
    """
    row = await database.fetch_one(query=query, values={"seller_id": seller_id})
    return dict(row) if row else None

# Creates a new seller
async def create_seller(user_id: int, brand_name: str):
    query = """
    INSERT INTO Sellers (user_id, brand_name)
    VALUES (:user_id, :brand_name)
    """
    try:
        seller_id = await database.execute(query=query, values={
            "user_id": user_id,
            "brand_name": brand_name
        })
        return seller_id
    except Exception:
        # Raise clear error if code already exists (email already in use)
        raise ValueError(f"Something went wrong with seller creation.")

# Updates an existing seller based on seller_id (user_id is immutable)
async def update_seller(brand_name: str, seller_id: int):
    query = """
    UPDATE Sellers SET brand_name = :brand_name
    WHERE seller_id = :seller_id
    """
    try:
        await database.execute(query=query, values={
            "brand_name": brand_name,
            "seller_id": seller_id
        })
        return True
    except Exception:
        # Raise clear error if code already exists (email already in use)
        raise ValueError(f"Error updating user")

# Deletes a seller based on seller_id
async def delete_seller(user_id: int):
    query = "DELETE FROM Sellers WHERE seller_id = :seller_id"
    try:
        await database.execute(query=query, values={"seller_id": user_id})
        return True
    except:
        return False