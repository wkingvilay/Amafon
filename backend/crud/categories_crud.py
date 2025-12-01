from database import database

# Returns all categories
async def get_categories():
    query = """
        SELECT * FROM Categories
    """
    return await database.fetch_all(query)

# Returns the name of a category based on category_id
async def get_category(category_id: int):
    query = """
        SELECT * FROM Categories WHERE category_id = :category_id
    """
    row = await database.fetch_one(query=query, values={"category_id": category_id})
    return dict(row) if row else None

# Creates a category (not reflected, but SQL tables don't have unique tag)
async def create_category(category_name: str):
    query = """
    INSERT INTO Categories (category_name)
    VALUES (:category_name)
    """
    try:
        category_id = await database.execute(query, values={"category_name": category_name})
        return category_id
    except Exception:
        raise ValueError(f"Category {category_name} already exists")

# Updates a category entry's name based on category_id
async def update_category(category_name: str, category_id: int):
    query = """
    UPDATE Categories SET
    category_name = :category_name
    WHERE category_id = :category_id
    """
    try:
        await database.execute(query, values={"category_name": category_name, "category_id": category_id})
        return True
    except Exception:
        raise ValueError(f"Error updating category")

# Deletes a category entry based on category name
async def delete_category(category_name: str):
    query = "DELETE FROM Categories WHERE category_name = :category_name"
    return await database.execute(query, values={"category_name": category_name})