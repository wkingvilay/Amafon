from ..database import database
from fastapi import APIRouter, HTTPException
from ..schemas.reviews import Reviews
from ..crud.reviews_crud import get_reviews_by_user, get_reviews_by_product, create_review, update_review, delete_review

router = APIRouter(prefix="/api/Reviews", tags=["Reviews"])

@router.get("/users_reviews/{user_id}", response_model=list[Reviews])
async def api_get_reviews_by_user(user_id: int, skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_reviews_by_user(user_id, skip, limit)
        return [Reviews(**dict(r)) for r in rows]

@router.get("/product_reviews/{product_id}", response_model=list[Reviews])
async def api_get_reviews_by_order(product_id: int, skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_reviews_by_product(product_id, skip, limit)
        return [Reviews(**dict(r)) for r in rows]

@router.post("/", response_model=Reviews)
async def api_create_review(review: Reviews):
    async with database:
        try:
            review_id = await create_review(review.product_id, review.user_id, review.rating, review.title, review.comment)
            row = await database.fetch_one(
                "SELECT * FROM Reviews WHERE review_id = :id",
                {"id": review_id}
            )
            return Reviews(**row)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        
@router.put("/", response_model=Reviews)
async def api_update_review(review: Reviews):
    async with database:
        try:
            await update_review(review.rating, review.title, review.comment, review.review_date, review.review_id)
            return Reviews(**dict(review))
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{review_id}")
async def api_delete_review(review_id: int):
    async with database:
        deleted = await delete_review(review_id)
        if not deleted:
            raise HTTPException(404, "Review not found")
        return {"detail": "Review deleted"}