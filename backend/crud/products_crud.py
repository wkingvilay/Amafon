from database import database

# TODO: still needs to aggregate reviews for a rating

# Returns information for a range of products (good for pages of items)
async def get_products(skip: int = 0, limit: int = 10):
    query="""
    SELECT * FROM Products
    LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query, values={'skip': skip,'limit': limit})

# Returns information for a specific product based on product_id
async def get_product(product_id: int):
    query="""
    SELECT * FROM Products
    WHERE product_id = :product_id
    """
    row = await database.fetch_one(query=query, values={"product_id": product_id})
    return dict(row) if row else None

# Creates a new product
async def create_product(seller_id: int, category_id: int, name: str, description: str, price: float, stock: int):
    query="""
    INSERT INTO Products (seller_id, category_id, name, description, price, stock)
    VALUES (:seller_id, :category_id, :name, :description, :price, :stock)
    """
    try:
        product_id = await database.execute(query=query, values={
            "seller_id": seller_id,
            "category_id": category_id,
            "name": name,
            "description": description,
            "price": price,
            "stock": stock
        })
        return product_id
    except Exception:
        raise ValueError(f"Product already exists")

# Updates an existing product based on product_id (seller_id is immutable)
async def update_product(category_id: int, name: str, description: str, price: float, stock: int, product_id: int):
    query="""
    UPDATE Products SET
    category_id = :category_id, name = :name, description = :description, price = :price, stock = :stock
    WHERE product_id = :product_id
    """
    try:
        await database.execute(query=query, values={
            "category_id": category_id,
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "product_id": product_id
        })
        return True
    except Exception:
        raise ValueError(f"Error updating product")

# Deletes a product based on product_id
async def delete_product(product_id: int):
    query="DELETE FROM Products WHERE product_id = :product_id"
    try:
        await database.execute(query=query, values={"product_id": product_id})
        return True
    except:
        return False

# Attempts to find products that have the keyword
async def search_product(key: str):
    query="""
    SELECT * FROM Products 
    WHERE LOWER(name) LIKE :key
    """
    search_key = f"%{key}%"
    return await database.fetch_all(query=query, values={"key": search_key})