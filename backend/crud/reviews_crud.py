from ..database import database
from datetime import datetime

# Returns any reviews from a user based off user_id
async def get_reviews_by_user(user_id: int, skip: int = 0, limit: int = 10):
    query = """
    SELECT * FROM reviews WHERE user_id = :user_id
    LIMIT :limit OFFSET :skip
    """
    return await database.fetch_all(query=query, values={"user_id": user_id, "skip": skip, "limit": limit})

# Returns any reviews of a product based off product_id
async def get_reviews_by_product(product_id: int, skip: int = 0, limit: int = 10):
    query = """
    SELECT * FROM reviews WHERE product_id = :product_id
    LIMIT :limit OFFSET :skip 
    """
    return await database.fetch_all(query=query, values={"product_id": product_id, "skip": skip, "limit": limit})

# Creates a new review
async def create_review(product_id: int, user_id: int, rating: int, title: str, comment: str):
    query = """
    INSERT INTO reviews(product_id, user_id, rating, title, comment)
    VALUES (:product_id, :user_id, :rating, :title, :comment)
    """
    try:
        await database.execute(query=query, values={
            "product_id": product_id,
            "user_id": user_id,
            "rating": rating,
            "title": title,
            "comment": comment
        })
        return await database.fetch_val("SELECT LAST_INSERT_ID();")
    except Exception:
        raise ValueError(f"Something went wrong with review creation.")

# Updates a review's rating and/or comment along with the timestamp
async def update_review(rating: int, title: str, comment: str, review_date: datetime, review_id: int):
    query = """
    UPDATE reviews SET rating = :rating, title = :title, comment = :comment, review_date = :review_date
    WHERE review_id = :review_id
    """
    try:
        await database.execute(query=query, values={"rating": rating, "title": title, "comment": comment, 
                                                    "review_date": review_date, "review_id": review_id})
        return True
    except:
        raise ValueError("Something went wrong with updating the review")

# Deletes a review based on review_id
async def delete_review(review_id: int):
    query = "DELETE FROM reviews WHERE review_id = :review_id"
    try:
        await database.execute(query=query, values={"review_id": review_id})
        return True
    except:
        return False